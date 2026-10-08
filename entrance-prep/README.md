# Entrance Prep · Mechanical Engineering @ RUPP

A practice platform for students preparing for the entrance examination. Students
create an account, work through multiple-choice sets in **Logic** and
**Mathematics**, and see immediately what they got right and wrong. Teachers
review and approve the question bank, build mock-exam blueprints, export papers
to Word or PDF, and see who has signed up and how the cohort is doing.

**Next.js + TypeScript**, **FastAPI + Python**, **SQLAlchemy**, PostgreSQL in
deployment and SQLite for local work. Originally built as a Logic-only tool
called Logic Studio; renamed when Mathematics was added.

This directory is self-contained. It shares the repository with the public ME
website but no code, database, or deployment — see the root
[`README.md`](../README.md).

## Subjects

| Subject | Domains | Seeded questions | Machine-provable |
|---|---|---|---|
| Logic & Reasoning | 7 | 84 | 48 |
| Mathematics | 7 | 84 | 84 |

Four levels throughout — Foundation, Practice, Exam Level, Challenge — against a
local rubric. These are preparation levels, not claims about official RUPP
standards. Physics is not built: the subject dimension is in place, but no
generator templates exist for it yet.

Every question is multiple choice with exactly 4 or 5 options, which is the
format of the real examination. Each option carries an internal misconception tag
and a rationale, so wrong answers are informative rather than filler.

## Run locally

Node.js 22+ and Python 3.11+. Two terminals, from this directory.

Backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:DEMO_MODE = 'true'
$env:AUTH_MODE = 'open'
# A separate file, so demo approvals cannot reach a real database.
$env:DATABASE_URL = 'sqlite:///./demo.db'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Frontend:

```powershell
cd frontend
npm ci
npm run dev
```

Then open **http://localhost:3000**.

`AUTH_MODE=open` is for local work only. It means no sign-in at all, and anyone
can switch to Teacher studio and read every answer key. Deployment uses
`AUTH_MODE=site`, where students must register and the studio is gated by role.
`DEMO_MODE` only pre-approves the sample bank; it is not an access control. Use
separate demo and real databases.

For macOS or Linux, use `.venv/bin/python` and `export` in place of `$env:`.

## Deploy

Docker Compose packages PostgreSQL 17, the API and the web service. Settings go
in `.env` beside `docker-compose.yml` — copy `.env.example` and fill it in; it is
gitignored and must never be committed.

```bash
docker compose up -d --build
```

The project name is pinned to `logic-studio` inside `docker-compose.yml`, which
is what the database volume is attached to. Do not change it: the stack would
come up against a new, empty database.

The web port binds to `127.0.0.1` only, so put HTTPS in front of it — currently
a Cloudflare Tunnel on the lab desktop. The database and API are never publicly
exposed. The API applies `alembic upgrade head` on start.

The full procedure, including what `PUBLIC_ORIGIN` must be and why a wrong value
refuses every write while reads keep working, is in
[`docs/DEPLOY-AND-OPERATE.md`](docs/DEPLOY-AND-OPERATE.md).

### Capacity

Measured on the lab stack: **250 students, 4,250 requests, 0 failures**, at 21
requests per second with 100 students in flight — registration 34 ms, answers
14 ms, submissions 7 ms at the median. Four API workers, a pool of 50 + 20 each,
PostgreSQL started with 300 connections. [`docs/CAPACITY.md`](docs/CAPACITY.md)
records how that was measured, including two mistakes in the measurement itself
that produced alarming numbers before the instrument was corrected.

## Teacher workflow

Nothing reaches a student unreviewed. A real installation seeds all 168 questions
as **drafts**, and a draft is invisible to students.

draft → review → approve or reject. Editing or regenerating returns a question to
draft. Approval requires passing structural checks **and** explicit teacher
attestation about wording, answer, explanation and distractors. Every transition
is written to an audit trail.

To approve the questions whose answers a machine can prove:

```bash
docker compose exec api python tools/approve_verified.py          # reports only
docker compose exec api python tools/approve_verified.py --apply
```

That approves **132** — all 84 Mathematics and 48 Logic — and leaves **36** as
drafts. Those 36 are the verbal and argument-reasoning questions, where no
machine can prove an answer, and they are exactly the ones a teacher must read.
What the tool certifies is that the server recomputed each answer from the
question's declared rule and it matched the key. It does not certify that the
wording is unambiguous or the difficulty label fair, so a teacher should still
skim. Approvals are recorded as `approved_machine_proved` with that caveat.

Teacher studio also holds the editable question bank with optimistic version
checks, mock-exam blueprints with exact allocations and capacity checks, the
student roster with CSV export, and aggregate analytics. Student responses never
include answer keys or teacher metadata.

Registration always creates a student, and the first teacher comes from
`TEACHER_EMAIL`. To give a colleague their own studio account they register
normally and are then promoted with `tools/make_teacher.py`, which is reversible
and audited in both directions.

## What it does, and what it does not claim

- **Practice**: immediate explanation, answer locked once checked.
  **Exam practice**: timed, answers editable until submission, feedback delayed.
  **Mock exam**: teacher-defined allocation, no repeated question. All three show
  a score and a right/wrong breakdown on submission.
- Scoring, deadlines and question snapshots are server-side. Unanswered counts as
  incorrect. Closing the browser does not stop the clock. Attempts are resumable
  and concurrent answer updates are guarded.
- Text, diagram and uploaded image questions; inline `$...$` LaTeX rendered with
  KaTeX. Worked maths is withheld until feedback is allowed.
- **Word and PDF export carry real mathematics.** `backend/app/mathtext.py`
  converts LaTeX to Office Math (OMML), so exported `.docx` equations are
  editable Word equations rather than source text, and PDF export uses Unicode
  mathematical characters. This was the original reason for building the
  platform: typing equations in Word by hand.
- Analytics come from completed attempts only — by topic, difficulty and chosen
  distractor tag. Students see their own results; teachers see aggregates. Error
  tags are learning indicators, not diagnoses.
- Responsive layouts and an install manifest. The service worker caches only an
  offline landing page; questions, saved answers and scoring need the network.

## Content provenance

The generator is **template based**. It does not call a language model and does
not read any textbook at run time: every question is parameterised and solved
independently. Template families are bounded on purpose, duplicate stems are
avoided within an option count, domain and difficulty, and an exhausted family
returns a capacity error rather than a repeat.

Two books informed the *structure* of the subjects, and nothing else. Logic
follows the reasoning families of LearningExpress's *501 Challenging Logic and
Reasoning Problems*, 2nd edition. Mathematics follows the topic structure of
Part One, Revision of Mathematics, of Bird & Ross, *Mechanical Engineering
Principles*, 3rd edition. No question is copied from either. Both PDFs stay
outside the application entirely — no route serves them and no bundle includes
them. Internal metadata records book, edition, publisher, ISBN, set family,
generation seed and the local calibration note. See `private/README.md` and
[`ARCHITECTURE.md`](ARCHITECTURE.md).

Three questions in the original local database were transcribed from the Logic
book and checked against the PDF, its answer key, and independent deterministic
rules; they are reachable only through *Question source: textbook selection* and
are labelled as adaptations once edited.

Deterministic validation covers arithmetic recurrences, letter steps, symbol
cycles, paired patterns, coded-language mapping, enumerated constraint ordering,
and — for Mathematics — recomputation of the stated expression against the key.
These checks verify structured rules and answers. They cannot certify that
natural-language wording matches the rule, so verbal and argument questions
require editorial review.

## Verify

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
cd ..\frontend
npm run typecheck
npm run build
# with a demo backend and the frontend running:
npx playwright install chromium
npx playwright test
```

39 backend tests. Coverage includes workspace separation, key stripping, review
transitions, stale edits, failed validators, immediate and delayed feedback,
immutable snapshots, expiry, attempt ownership, exact blueprint allocation,
server scoring, CSRF and the origin guard, exports, subject filtering, the
student roster, and anonymous-visitor isolation. Set `CHROME_PATH` to use an
installed Chrome instead of downloading Chromium. Browser tests mutate a demo
bank — never point them at a real student database.

## Known gaps

Honest list, in the order they are likely to bite:

- **No password reset.** With 250 students, somebody will be locked out in the
  first week, and today the only remedy is a database edit.
- **No registration code and no email verification**, so anyone with the link can
  create an account with any address.
- **No frozen assignment**: every student gets a freshly generated set, so two
  students cannot be compared question by question.
- **36 Logic questions remain unapproved** pending editorial review, and 10 of
  the approved ones share a stem with another.
- **No Physics templates.**
- No delete-account path, no remote asset storage, no proctoring.

Institutional use needs database backups, reverse-proxy rate limits and teacher
content review before the bank is widened.
