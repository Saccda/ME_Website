# What is built, and what is next

Updated 2026-10-08, after the lab stack carried 250 students with no failures.
This supersedes the proposal written on 2026-10-02.

## Done

| | |
|---|---|
| **Student sign-up** | Name, email, password. No student ID — deliberately, so registration is one screen. `AUTH_MODE=site` gates Teacher studio by role. |
| **Results on submission** | Score, percentage, and a correct / incorrect / not-answered breakdown; the question navigator colours green, red or grey with screen-reader labels. This was the reported bug: submitting an exam used to tell you nothing. |
| **Subject dimension** | `Question.subject`, migration `0002`, `?subject=` filtering on questions, availability, attempts and analytics, a subject dropdown for students, and per-subject seeding so a new subject fills on the next start without touching what is there. |
| **Mathematics** | 7 domains, 28 templates across four levels, following the topic structure of Bird & Ross Part One. 84 of 84 machine-provable, because the server recomputes every answer. |
| **Physics** | 7 domains, 28 templates, scoped to the examination's own physics section, which is electrical rather than mechanical. 84 of 84 machine-provable: the computational ones by recomputation, the conceptual ones against a reviewed table of units, instruments and source behaviour. |
| **Exam shape** | The real paper is 80 questions in 90 minutes — 25 Mathematics, 25 Logic, 30 Physics. Practice offers that section length as one tap. |
| **Mock exam** | A blueprint row may name a whole subject, so the real paper is three rows. `tools/create_exam_blueprint.py` builds and publishes it. Sections are sat in order rather than interleaved, and the result is reported per section as well as in total. |
| **LaTeX → Word and PDF maths** | `backend/app/mathtext.py` converts LaTeX to Office Math (OMML), so exported `.docx` equations are editable Word equations, and to Unicode for PDF. Dependency-free. This was the original reason for the project. |
| **Deployment** | PostgreSQL 17, four API workers, advisory-locked startup seeding, `max_connections=300`, pinned Compose project name, Cloudflare Tunnel, and a button on the ME website's Admissions page that appears only when the URL is set in Wagtail. |
| **Capacity, measured** | 250 students, 4,250 requests, 0 failures. See [`CAPACITY.md`](CAPACITY.md). |
| **Teacher tooling** | `approve_verified.py` approves only machine-proved questions; `remove_test_accounts.py` clears load-test accounts; a Students roster with CSV export. |
| **Logic bank audit** | All 36 unproven answer keys checked by hand and found correct; six defect classes fixed at template level. See [`LOGIC-BANK-AUDIT.md`](LOGIC-BANK-AUDIT.md). |

## Next, in the order I would do them

### 1. Password reset — teacher-issued

The only gap that locks a real student out. An email reset needs an SMTP service
the project does not have, and addresses are unverified anyway. A teacher-issued
reset needs no mail server:

- A **Reset password** action on the existing Students list.
- The teacher gets a one-time code to hand over; it expires in 24 hours and works
  once.
- The student enters the code and chooses a new password.
- Every reset is audited, with who did it.

This fits a university cohort, where staff already know who the students are. An
email reset can be added later without changing the model.

### 2. Frozen assignment, and a class results grid

Today every student gets a freshly generated set, so no two students can be
compared question by question — which was the point of the original plan to post
the same exercises in a shared sheet.

A teacher creates an **assignment**: a fixed, ordered list of question ids,
published to the cohort. Every student gets the same paper. The teacher then sees
one grid — students down the side, questions across the top — which is the
shared-sheet idea with the marking done for them, and it makes "question 7 was
badly worded" visible immediately.

### 3. Registration code

Anyone with the link can register today, with any address and no limit.

- A code per intake, for example `ME-2026-ENTRY`, with an expiry and a maximum
  number of uses.
- Registration requires it; a wrong code is refused.
- Per-IP rate limiting on `POST /api/auth/register` — login is already throttled
  at 10 failures per email per 15 minutes, registration is not throttled at all.

That also removes the need to verify email addresses, and records which intake a
student belongs to. A real cohort signing up together is indistinguishable from
an attack, so a code admits the class and excludes everyone else — better than a
rate limit that would block the class itself.

### 4. A conditional-logic validator

Nine of the 36 unproven questions — `necessary-condition`, `must-be-true` and
`multi-condition-judgment` — are formal conditional logic: universal
conditionals plus a fact about one person, asking what must follow. That is
mechanically checkable the same way the `ordering` family already is, by
enumerating the models consistent with the premises and confirming exactly one
option holds in all of them.

It would move nine questions from "trust the author" to "proved", and every
future question in those families with them. The remaining 27 rest on meaning
rather than form and will always need a teacher's eye.

### 5. A frozen assignment, so students can be compared

Built in its place: the mock exam below. What it does not do is give two
students the *same* paper — each sitting draws its own questions, so a cohort
cannot be compared question by question. See item 2.

### 6. De-duplicate practice sets by stem

Five stems are each shared by two approved questions, because the seed signature
is `(stem, option count)` and so the same stem seeds twice — once with four
options, once with five. A mock exam draws by question id, which does not stop
both twins appearing on one paper. De-duplicating by stem at assembly time fixes
the student-facing symptom whatever the bank contains.

### 7. One-press practice start

Before answering anything a student faces seven decisions: question source,
domain, difficulty, skill, option count, question count, and for exams a time
limit. Most of those only a teacher has an opinion about.

```
  [ Start practising ]        ← 10 mixed questions at your current level
  ▸ Choose topic and level     ← opens today's full form, unchanged
```

The overview could also carry the next action — continue the unfinished session,
practise the weakest topic, take the next mock exam. The analytics needed to pick
a weakest topic already exist.

## Decide before launch, not after

You are now storing student names and email addresses. Worth settling: what the
data is used for, how long it is kept, who can see it, and how a student asks for
their account to be deleted. There is no delete-account path today.
