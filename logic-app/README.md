# Logic Studio · Mechanical Engineering @ RUPP

A runnable web-first Logic preparation application: **Next.js + TypeScript**, **FastAPI + Python**, **SQLAlchemy**, SQLite for local use and PostgreSQL for deployment. The official project assets and Digital Brand System informed the blue/white/gold identity and educational voice. Synced files under `sources/` were left untouched.

## Run locally

Requires Node.js 22+ and Python 3.11+. Open two terminals from this directory. `backend/requirements.lock.txt` records the exact Python versions tested here; use it in place of `requirements.txt` for a pinned install. The frontend's `package-lock.json` is included for `npm ci`.

Backend, PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:DEMO_MODE = 'true'
$env:AUTH_MODE = 'open'
# Use a separate file so demo approvals cannot enter your real database.
$env:DATABASE_URL = 'sqlite:///./demo.db'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Frontend, a second terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Open **http://localhost:3000**. The student workspace opens immediately. There is no login, registration, or password screen. Use **Student workspace / Teacher studio** in the sidebar to switch workspaces. On mobile, open the menu first. `AUTH_MODE=open` is the default. `DEMO_MODE` controls sample-question approval only; it does not control access or require demo credentials.

An anonymous HttpOnly browser cookie saves progress for 30 days, renewed when the workspace opens. Each browser has separate progress, and switching to Teacher studio and back preserves that browser's student attempts. Clearing cookies or using a different browser starts a new learner history. This is browser-based progress, without an account or cross-device identity.

For macOS/Linux, replace the Python executable with `.venv/bin/python` and environment assignments with `export DEMO_MODE=true` and `export DATABASE_URL=sqlite:///./demo.db`.

For a normal installation, copy `.env.example` to `.env`, use a new database, and start the backend with:

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --env-file ../.env --host 127.0.0.1 --port 8000
```

Without demo mode, all 84 original starter questions begin as drafts. Teacher workflow: draft → review → approve or reject. Editing or regeneration returns the question to draft. Approval requires passing structural checks **and** explicit teacher attestation about wording, answer, explanation, and distractors. Existing approved demo records are not automatically downgraded by changing an environment flag; always use separate demo and real databases.

## Included behavior

- Seven student-facing domains: Number & Pattern Reasoning; Letter & Symbol Reasoning; Classification & Relationships; Coded Language Reasoning; Applied Verbal Reasoning; Deductive Logic & Logic Games; Critical & Argument Reasoning.
- Foundation, Practice, Exam Level, and Challenge, with a local rubric. These are preparation levels, not claims about official RUPP exam standards.
- MCQ-only, exactly 4 or 5 options. Domain, difficulty, and skill filters; bounded original question generation. Each option has an internal misconception tag and rationale.
- Teacher studio, editable question bank, optimistic review version checks, rejection reasons, regeneration, and audit history. Student-workspace responses exclude answer keys and teacher metadata. In open mode, any visitor can deliberately switch to Teacher studio; workspace selection is not an access restriction.
- Text, diagram, and uploaded PNG/JPEG/WebP questions, with image alt text/credit; inline `$...$` LaTeX via KaTeX. Math in worked explanations is withheld until feedback is allowed.
- Practice: immediate explanation, locked answer after checking. Exam practice: timed, editable saved answers, delayed feedback. Mock exams: exact teacher-defined allocations, no repeated question ID, approved-bank capacity checks, published/draft visibility, and editable blueprints.
- Server-side scoring, server deadlines, resumable attempts, immutable question snapshots, final submission, and guarded concurrent answer updates. Unanswered questions count as incorrect. A disconnected browser cannot stop the server deadline.
- Real analytics from completed attempts, by topic, difficulty, and selected distractor tags. Students see their own results; teachers see aggregate results. Error tags are possible learning indicators, not psychological diagnoses.
- Teacher-workspace DOCX/PDF exports: question paper, key, and worked solutions. Original/licensed images and diagram tables are included; private source metadata is excluded.
- Responsive layouts, install manifest, and a service worker that caches only an offline landing page. Online access is required for questions, saved answers, and scoring.

## Content provenance and limits

The private reference is LearningExpress's *501 Challenging Logic and Reasoning Problems*, 2nd edition. The actual attachment was read from the referenced chat; its requested `/mnt/data/` path is unavailable on this Windows host. The default seed contains 84 original questions. This local database also includes three user-selected textbook questions checked against the PDF transcription, answer key, and independent deterministic rules. Choose Question source: Textbook selection in practice. Explanations and distractor rationales are newly authored, with visible attribution. The whole PDF remains private. Internal metadata keeps the book, edition, publisher, ISBN, set family, generation seed, and local calibration note. See `private/README.md` and `ARCHITECTURE.md`.

The generator is **template based**, with parameterized original facts and reasoning; it does not call an LLM or search the textbook. Template families are intentionally bounded. Generation avoids duplicate stems for the same option count/domain/difficulty and returns a useful capacity error if the family is exhausted. A selected skill must match its difficulty; the studio shows the default level-appropriate skill. Regeneration produces a new seeded variant of the same family. Teachers can completely rewrite a draft to author new content.

Deterministic validation covers arithmetic recurrence sequences, letter steps, symbol cycles, paired patterns, coded-language mapping, and enumerated constraint/conditional ordering. These checks verify structured rules and the answer key. They cannot certify that natural-language wording matches the rule or that an explanation is pedagogically sufficient. Verbal/argument questions require editorial review. The sample bank and local level rubric need RUPP teacher review before live student use.

DOCX/PDF adapters currently render prose and ordinary Unicode symbols; formulas authored with `$...$` are exported as source text, not typeset equations or editable Word math. The browser renders full KaTeX. Equation-native DOCX/PDF rendering is an explicit adapter boundary; exports do not silently claim parity with browser math.

## Verify

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
cd ../frontend
npm run typecheck
npm run build
# Start a demo backend and the frontend first, then:
npx playwright install chromium
npx playwright test
```

To use an installed Chrome, set `CHROME_PATH` to its executable instead of downloading Chromium. Browser tests mutate a demo bank and create anonymous sample attempts; never run them against a real student database. Backend tests use their own `test-logic.db`. Coverage includes workspace separation, source/key stripping, review transitions, stale edits, failed validators, immediate/delayed feedback, immutable snapshots, expiration, attempt ownership, exact blueprint allocation, server scoring, CSRF, exports, and anonymous visitor isolation. The old credential-mode API compatibility is separately tested. Browser tests cover direct no-login entry, teacher review/editing, student practice, exam feedback, mock start, mobile fit, and progress across reloads and workspace switches.

## Deploy

Docker Compose packages PostgreSQL, the API, and the web service. Set actual secrets and `PUBLIC_ORIGIN` in `.env`, then run `docker compose up --build -d`. The web port binds to `127.0.0.1:3000`; put an HTTPS reverse proxy in front of it. The database and API are not publicly exposed. Compose disables demo mode, enables secure cookies, and runs Alembic migrations before API startup. Configure database passwords without URL-reserved characters or URL-encode the password in the DSN.

The Docker configuration is provided but has not been run in this Windows session. Local SQLite, the production Next.js build, backend tests, and browser tests were exercised. PostgreSQL-compatible types and an initial migration are included; validate your deployment environment before admitting real users.

Set `DB_AUTO_CREATE=false` for deployment and apply migrations with `python -m alembic upgrade head`. Local startup can create a fresh schema automatically. For an existing auto-created **v1** schema, `python -m alembic stamp 0001` records the baseline without rebuilding tables. Back up before applying any future migration. Never stamp a schema that differs from the supplied v1 models.

This standalone version intentionally leaves Teacher studio open, as requested. Before putting it on the public official ME website, connect teacher access to the website's trusted identity or restrict the studio at the website boundary. Student practice can remain open. The integration point is `POST /api/workspace` and the `current_user` dependency; it is not yet connected to the existing website. The actual textbook remains outside all application routes and the source bundle.

Institutional rollout needs an HTTPS host, database backups, reverse-proxy rate limits, and teacher content review. There is no remote asset storage or high-stakes exam proctoring. No external hosting or website integration was performed.

Official framework references: [Next.js installation](https://nextjs.org/docs/app/getting-started/installation), [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/).

### Optional checked textbook selection

The portable archive excludes the private selection payload and database. From backend/, with the server DATABASE_URL configured, run `python tools/import_textbook_selection.py --selection ../private/textbook-selection.json --pdf <your-private-PDF-path>` to restore a supplied selection. Repeat imports preserve existing records. Editing an excerpt labels it as an adaptation and clears book-key verification.
