# What is built, and what is next

Updated 2026-10-08, after the lab stack carried 250 students with no failures.
This supersedes the proposal written on 2026-10-02.

## Done

| | |
|---|---|
| **Student sign-up** | Name, email, password. No student ID — deliberately, so registration is one screen. `AUTH_MODE=site` gates Teacher studio by role. |
| **Results on submission** | Score, percentage, and a correct / incorrect / not-answered breakdown; the question navigator colours green, red or grey with screen-reader labels. This was the reported bug: submitting an exam used to tell you nothing. |
| **Subject dimension** | `Question.subject`, migration `0002`, `?subject=` filtering on questions, availability, attempts and analytics, a subject dropdown for students, and per-subject seeding so a new subject fills on the next start without touching what is there. |
| **Mathematics** | 7 domains, 28 templates across four levels, following the topic structure of Bird & Ross Part One. About 330 questions, all machine-provable, because the server recomputes every answer. |
| **Bank size, weighted by the real paper** | `EXAM_WEIGHTS` in `catalog.py` records how many of the real paper's questions each sub-topic carries, from the panel's own control sheets for Logic and Mathematics and from the bank's section sizes for Physics. The seeder divides a per-subject budget of 300 by those weights, so Calculus — 14 of the 25 Mathematics marks — gets 48 questions a level while Units, which the sheet does not examine, gets the floor of 3. A flat target of 12 gave them the same and pushed Physics to 812. Templates are bounded and differ enormously (`units` yields 4 distinct questions, `algebra` 478), so a slot that cannot reach its target stops early. Unprovable families are held at 3 however heavily weighted, because each is a question a teacher must read. Seeding tops up towards the target on every start; `tools/prune_to_target.py` brings an over-full bank down, sparing anything a student has already been served. Landed at Logic 156, Mathematics about 330, Physics 341, plus the panel's untouched 100. |
| **Physics** | 19 domains, 76 templates, 228 of 228 machine-provable. Seven electrical sub-topics follow the past paper; five covering motion, forces, mechanical work, fluids and heat follow the topic structure of Mukherji Parts 1–2; seven more — momentum, rotation, thermodynamic processes, fluid flow, waves, fields and AC reactance — follow the sections of the examination panel's own bank. The computational ones are proved by recomputation, the conceptual ones against a reviewed table. |
| **The examination panel's bank** | The panel's 100 physics questions, loaded by `tools/import_exam_bank.py` from `private/exam_bank.json`, which is deliberately not in this public repository. All 100 keys were checked before import: the 29 computable ones are recomputed by the server on every import, the rest were verified by hand. 70 of the 100 had no sub-topic to sit in, which is why the seven above exist. The panel's own letter distribution was A 34 / B 57 / C 9 / **D 0**, so answering B blind scored 57/100; option order is redistributed on import so each letter is correct 25 times, with wording and keys untouched. |
| **Exam shape** | The real paper is 80 questions in 90 minutes — 25 Mathematics, 25 Logic, 30 Physics. Practice offers that section length as one tap. |
| **Four choices, everywhere** | The paper offers four, so every question does: practising five rehearses a shape no student will sit and changes the odds of a guess. The seeder makes only four-option questions, `tools/to_four_options.py` converts any that already exist, and the choice is gone from the practice, generation and blueprint forms. This also removed the duplicate-stem defect listed here before: the seed signature carried the option count, so one stem could seed twice — once with four options, once with five — and five pairs of approved questions shared a stem. The signature is now the stem alone. |
| **Mock exam** | A blueprint row may name a whole subject, so the real paper is three rows. `tools/create_exam_blueprint.py` builds and publishes it. Sections are sat in order rather than interleaved, and the result is reported per section as well as in total. A row may also name an **origin**, and the physics section uses it to draw only the panel's own questions: a generated question is honest practice for a topic, but the panel's items are the paper itself. `--mixed-physics` widens it to the generated bank. Every sitting draws afresh, so a student who sits it twice gets a different paper; how different depends on the pool. Measured over 12 sittings: 15 of the 80 questions repeat between any two, so 82% of each paper is new. Mathematics draws 25 from 300 and Logic 25 from 228; Physics draws 30 from the panel's 100, which is now the narrowest section and is deliberately so. |
| **LaTeX → Word and PDF maths** | `backend/app/mathtext.py` converts LaTeX to Office Math (OMML), so exported `.docx` equations are editable Word equations, and to Unicode for PDF. Dependency-free. This was the original reason for the project. |
| **Deployment** | PostgreSQL 17, four API workers, advisory-locked startup seeding, `max_connections=300`, pinned Compose project name, Cloudflare Tunnel, and a button on the ME website's Admissions page that appears only when the URL is set in Wagtail. |
| **Capacity, measured** | 250 students, 4,250 requests, 0 failures. See [`CAPACITY.md`](CAPACITY.md). |
| **Teacher tooling** | `approve_verified.py` approves only machine-proved questions; `remove_test_accounts.py` clears load-test accounts; `to_four_options.py` and `import_exam_bank.py` maintain the bank; a Students roster with CSV export, and `roster.py` for the same from the command line — which also counts the unfinished sessions the screen ignores, since practice has no time limit and a student can answer and simply close the tab. |
| **Logic bank audit** | All 36 unproven answer keys checked by hand and found correct; six defect classes fixed at template level. See [`LOGIC-BANK-AUDIT.md`](LOGIC-BANK-AUDIT.md). |
| **Password reset** | Self-service by emailed six-digit code, one hour, single use, five attempts, throttled per address, and every existing session signed out on success. Off unless SMTP is configured, so no deployment offers a reset it cannot send. |

## Next, in the order I would do them

### 1. The 10 Mathematics marks with no practice behind them

The panel's control sheet names eight Mathematics topics over 25 questions.
Four of them have no template, and together they are **10 of the 25 marks**:

| Marks | Topic on the sheet | What exists |
|---|---|---|
| 3 | Linear Algebra / Determinants | nothing — no sub-topic at all |
| 3 | Vector Algebra / Dot & Cross Product | `vectors` does components, magnitude, direction, addition |
| 2 | Algebra and Function / Quadratic | `algebra` does brackets, indices, linear and simultaneous equations |
| 2 | Calculus / Limit | `calculus` does differentiation, rates, integration, definite integrals |

A student can practise 15 of the 25 marks and not the other 10. That is a
larger gap than anything else on this list, and all four are computable, so
every question would be machine-proved like the rest.

Three existing sub-topics — Number & Proportion, Angles & Triangles, Units &
Engineering Notation — are not on the sheet at all. They stay at the floor
because they are the groundwork the examined topics stand on, but they should
not grow.

### 2. Classification carries 11 of 25 Logic marks and cannot be proved

`relationships` — Verbal Classification, Essential Part and Analogies, sets
7–17 — is the heaviest sub-topic in either control sheet, and the one with the
least behind it: its template yields 8 distinct questions and no validator can
check a meaning-based answer, so it is held to 12 questions that a teacher had
to read by hand. Raising it to its ceiling of 32 would need 20 more reviewed.
Widening the template matters more than raising the cap.

### 3. Email verification at sign-up

Built instead of the teacher-issued reset that was planned here: a student
resets their own password with a six-digit code emailed to them, which needs
nobody's time. The teacher-handover version was dropped because distributing
codes to 250 students is a job nobody has.

What remains is the one gap it cannot close. Addresses are never verified, so a
student who mistypes theirs at sign-up can neither receive a code nor be found
in the roster under the address they think they used. Verifying at registration
— the same code mechanism, run at a different moment — fixes that and removes
most of the need for a registration code at the same time.

### 4. Frozen assignment, and a class results grid

Today every student gets a freshly generated set, so no two students can be
compared question by question — which was the point of the original plan to post
the same exercises in a shared sheet.

A teacher creates an **assignment**: a fixed, ordered list of question ids,
published to the cohort. Every student gets the same paper. The teacher then sees
one grid — students down the side, questions across the top — which is the
shared-sheet idea with the marking done for them, and it makes "question 7 was
badly worded" visible immediately.

### 5. Registration code

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

### 6. A conditional-logic validator

Nine of the 36 unproven questions — `necessary-condition`, `must-be-true` and
`multi-condition-judgment` — are formal conditional logic: universal
conditionals plus a fact about one person, asking what must follow. That is
mechanically checkable the same way the `ordering` family already is, by
enumerating the models consistent with the premises and confirming exactly one
option holds in all of them.

It would move nine questions from "trust the author" to "proved", and every
future question in those families with them. The remaining 27 rest on meaning
rather than form and will always need a teacher's eye.

### 7. A frozen assignment, so students can be compared

Built in its place: the mock exam below. What it does not do is give two
students the *same* paper — each sitting draws its own questions, so a cohort
cannot be compared question by question. See item 2.

### 8. One-press practice start

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
