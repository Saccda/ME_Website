# Deploying and operating Entrance Prep

The stack runs in Docker on the lab desktop: PostgreSQL 17, the FastAPI service
with four workers, and the Next.js web service bound to `127.0.0.1` behind a
Cloudflare Tunnel. Nothing here touches the `me-rupp` stack — separate project
name, separate port, separate database.

Every command below is run from `entrance-prep/` on the lab desktop.

## 0. If you are pulling the rename

This directory used to be called `logic-app`. `git pull` creates
`entrance-prep/` and removes the tracked files from `logic-app/`, but **it
cannot move your `.env`**, because that file is gitignored and git does not know
it exists. It will be left behind in the old folder.

```powershell
move logic-app\.env entrance-prep\.env
```

Then check that `logic-app/` holds nothing else you want — it will still contain
build leftovers such as `node_modules`, `.next` and `.venv`, all of which are
rebuilt inside the images and can be deleted.

The Compose project name is pinned inside `docker-compose.yml`, so `-p` is no
longer needed on the command line — though passing it does no harm.

## 0b. If you are pulling the project rename

The project was called `logic-studio` until the name was changed to
`entrance-prep`. **That is a migration, not an edit.** The project name is what
Compose attaches the volume to, so the new name means a new, empty volume while
the old database sits in `logic-studio_logic-data`.

It was done while the database held nothing but the question bank, one teacher
and one blueprint, all three of which rebuild themselves. So:

```bash
docker compose -p logic-studio down
```

```bash
docker compose up -d --build
```

The API creates the schema, seeds all 312 questions as drafts, and recreates the
teacher from `.env`. Then approve the bank and rebuild the paper (§4 and §5),
and confirm Docker Desktop shows `entrance-prep` rather than `logic-studio`.

Only once the new stack is working, reclaim the old volume:

```bash
docker volume rm logic-studio_logic-data
```

**Never do this again after students have accounts.** Copy the volume instead:
`docker volume create <new>_data` then
`docker run --rm -v <old>_logic-data:/from -v <new>_data:/to alpine sh -c "cd /from && cp -a . /to"`.

## 1. Settings

`.env` goes **beside `docker-compose.yml`**, not in `backend/`. (`backend/.env`
is a different file, used only when running the API directly without Docker.)
Copy `.env.example` and fill it in. It is gitignored; never commit it.

Write values with no space after `=`, or the space ends up inside the password.

### For real student use

```
POSTGRES_PASSWORD=<a long unique password>
TEACHER_EMAIL=<the first teacher's address>
TEACHER_PASSWORD=<at least 12 characters>
AUTH_MODE=site
WEB_PORT=3100
PUBLIC_ORIGIN=https://prep.your-domain.example
COOKIE_SECURE=true
```

### For a local test first, over plain HTTP

Change two lines:

```
PUBLIC_ORIGIN=http://127.0.0.1:3100
COOKIE_SECURE=false
```

`COOKIE_SECURE=false` **matters here.** A Secure cookie is not stored over plain
HTTP, so with it left at `true` a sign-in over `http://127.0.0.1` appears to
succeed and the session silently vanishes — and a load test fails at its first
authenticated call for the same reason.

### What PUBLIC_ORIGIN must be

It becomes `APP_ORIGINS`, which the write guard compares **literally** against
the browser's `Origin` header. It must be exactly what appears in the address
bar: scheme, host, and port if non-standard. **No trailing slash, no path.** Get
it wrong and every write is refused with "Request origin could not be verified"
while reads keep working — a confusing failure, because the site loads normally
and then nothing can be saved.

A comma-separated list is accepted if you need two origins while testing, but
`COOKIE_SECURE` can only suit one of them, so prefer testing and going live as
two separate steps.

`AUTH_MODE=site` is what requires students to sign up. Leave it as `open` only
if you want no sign-in at all — in that mode **any visitor can open Teacher
studio and read every answer key**.

`TEACHER_EMAIL` and `TEACHER_PASSWORD` are not optional. With sign-up enabled
and demo mode off, the API refuses to start without them, because there would be
no way to review or approve anything.

## 2. Publishing the address

Add a Cloudflare Tunnel hostname pointing at the web port, the same pattern
already used for the ME API (`me-api.farmos-mechanicalengineering.com`).

**The lab desktop's tunnel is managed from the Cloudflare dashboard, not from a
file.** Check before editing anything:

```bash
sc.exe qc Cloudflared
```

If `BINARY_PATH_NAME` contains `--token`, which it does on the lab desktop, then
`cloudflared` fetches its ingress rules from Cloudflare's API and **ignores local
ingress rules entirely**. There is a stale `config.yml` in
`C:\Windows\System32\config\systemprofile\.cloudflared\` which is inert; editing
it does nothing, and it has misled us once already.

So add the hostname in the dashboard: **Zero Trust → Networks → Tunnels →** the
tunnel **→ Edit → Published application routes → Add a public hostname**.

| Field | Value |
|---|---|
| Subdomain | `prep` |
| Domain | your domain |
| Path | empty |
| Type | `HTTP` |
| URL | `127.0.0.1:3100` |

It applies within seconds, **no restart**, and the DNS record is created for you,
so `cloudflared tunnel route dns` is not needed either. Rule ordering is the
dashboard's problem rather than yours.

Type is `HTTP` even though students arrive over HTTPS: Cloudflare terminates TLS
at the edge and the hop to the container on the same machine is plain HTTP. That
does not affect `COOKIE_SECURE=true`, because the browser only ever sees
`https://`.

Only if `BINARY_PATH_NAME` shows `--config <path>` instead is the tunnel
locally managed. Then the rule goes in that file, with the `http_status:404`
catch-all kept last, followed by a DNS route and a service restart
(`net stop Cloudflared && net start Cloudflared`, elevated).

Either way, the service token is a credential: it carries the tunnel secret, and
anyone holding it can run a connector for the tunnel. Never paste it into a
chat, an issue or a commit. If it leaks, refresh it in the dashboard and
reinstall the service.

### Publishing the button

Put the URL into Wagtail under **Settings → Program settings → Entrance
preparation platform URL**. The ME website's Admissions page shows the button
only when that field is set, so leaving it empty keeps the platform reachable by
link alone — which is what you want while a small group tests it.

## 3. Bring it up

```bash
docker compose up -d --build
docker compose ps
docker compose logs api --tail 40
curl http://127.0.0.1:3100/api/health
```

The API applies `alembic upgrade head` on start, so the schema is created and
migrated for you (currently through `0004`). Startup seeding is wrapped in a
PostgreSQL advisory lock, so the four workers cannot seed the bank twice.

Confirm the workers actually started — `logs api` should show four
`Started server process` lines.

## 3a. Bring an over-full bank back to the examination's shape

Only needed on an installation seeded under the old flat target, which put 812
questions in Physics spread evenly over sub-topics worth between 1 and 15 marks.
Seeding only ever adds, so lowering a target stops growth without shrinking
what is there.

```bash
docker compose exec api python tools/prune_to_target.py          # reports only
docker compose exec api python tools/prune_to_target.py --apply
```

Run it after the restart, so the under-served sub-topics have already been
topped up, and before the approval step below, so you are not approving
questions you are about to remove. The two converge: running either again does
nothing. Expect roughly 650 removed, leaving Logic 156, Mathematics 331 and
Physics 341 beside the panel's untouched 100.

It removes only questions **no student has ever been served**, newest first. A
question that has appeared in somebody's attempt stays, even if that leaves its
sub-topic over target, because the per-question report is built from those
attempts. Imported questions are never touched.

## 4. Approve something to practise — do not skip this

A fresh installation seeds **about 826 questions, none approved**. The exact
figure moves by a question or two between installations, because a template
that is nearly exhausted may or may not find one more distinct stem within its
allowed draws. That is the correct
default, since nothing should reach a student unreviewed, but on launch day a
student would otherwise get

> Only 0 approved questions match. Reduce the count or broaden your filters.

```bash
docker compose exec api python tools/approve_verified.py          # reports only
docker compose exec api python tools/approve_verified.py --apply
```

Measured result: **790 approved** (329 Mathematics, 341 Physics, 120 Logic),
**36 left as drafts**.

Run it again after any release that adds sub-topics **or changes how many
questions each one holds** — both reshape the bank at startup as drafts, so
they need approving too. That count has moved three times: from 276 when seven
Physics sub-topics arrived, from 360 when each slot went from three questions
to twelve, and again when the targets were weighted by the examination's own
control sheets instead of being flat.

The 36 are the `editorial` ones — verbal and argument
reasoning, where no machine can prove an answer — and they are exactly the
questions a teacher must read. They stay invisible to students until approved in
Question bank, and until then those three Logic sub-topics show as "none
approved yet" and cannot be selected.

The tool certifies that the server recomputed each answer from the question's
declared rule and it matched the key. It does **not** certify that the wording is
unambiguous, the distractors plausible, or the difficulty label fair. Every
approval is recorded in the audit trail as `approved_machine_proved` with that
caveat.

## 4a. Bring older questions down to four options

The entrance paper offers four choices. New questions are seeded that way, but
the seeder only fills a sub-topic that is empty, so an installation that was
set up before this change still holds five-option questions — one per
sub-topic and level, 132 of them on a full bank.

```bash
docker compose exec api python tools/to_four_options.py          # reports only
docker compose exec api python tools/to_four_options.py --apply
```

It removes one wrong option, shuffles the four that remain, and re-letters them.
The stem, the answer and the worked explanation are untouched, every converted
question is re-validated before it is written, and anything that would no longer
pass is left alone and reported. Attempts already sat keep their own snapshot,
so a paper a student is part-way through is unaffected.

The shuffle matters: keeping the order meant every question whose answer had
been E came out with its answer at D, putting 39% of converted answers on one
letter.

## 4b. Load the examination panel's physics bank

The panel's own 100 physics questions are **not in this repository**, and must
not be: the GitHub remote is public, and these are the questions the real paper
draws on. They live in `entrance-prep/private/exam_bank.json`, which
`.gitignore` already covers, and the file is carried to the lab by hand.

Put the file in `entrance-prep/private/` on the lab, then:

```bash
docker compose exec api python tools/import_exam_bank.py          # reports only
docker compose exec api python tools/import_exam_bank.py --apply
```

`private/` is bind-mounted read-only into the container at `/app/private`, so
the tool finds the file without it ever entering the image.

Every question is put through the same validator the generators are held to,
and the whole file is refused if any one of them fails, rather than importing
the good ones and leaving a bank nobody can account for. The 29 computable
answers carry a `compute` spec and are recomputed on every run. They arrive
**approved**, unlike generated seeds, because the author is the examination
panel and the keys were checked item by item; pass `--draft` to review them in
Teacher studio first.

Re-running updates what it imported before rather than adding a second copy,
matching on the `ref` recorded in each question's source, so it is safe after
the panel revises an item.

One thing the import changes on purpose: in the panel's file the correct answer
is A 34 times, B 57, C 9 and **D never**, so a student who noticed could score
57/100 by answering B without reading a question. Option order is redistributed
so each letter is correct 25 times. Wording, options and keys are unchanged.

## 5. The mock exam that matches the real paper

80 questions in 90 minutes — 25 Mathematics, 25 Logic, 30 Physics, four options
each, sat in that order. One command builds it:

```bash
docker compose exec api python tools/create_exam_blueprint.py          # reports only
docker compose exec api python tools/create_exam_blueprint.py --apply
```

The physics section draws on the panel's bank above, so step 4b has to come
first. A generated question is honest practice for a topic; the panel's items
are the paper itself, which is the point of sitting a mock. Mathematics and
Logic have no panel bank and draw on the generated one. `--mixed-physics`
widens physics to the generated bank too.

It refuses to publish a paper the bank cannot fill and names the short section.
Re-running updates the paper it made before rather than adding a second one, so
it is safe to run again after approving more questions. `--draft` saves it
unpublished if you want to look before students can.

Students find it under **Mock exams**. On submission they get a score per
section — Mathematics 18 / 25, Logic 20 / 25, Physics 22 / 30 — the way the real
paper is marked, as well as the total.

Teacher studio can build other papers the same way: a blueprint row may name a
whole subject, or a single sub-topic and level as rows always could.

## 5b. Password reset by email

Without this a student who forgets their password registers again with another
address, keeping none of their history and leaving you a duplicate in the
roster. With it they reset it themselves and nobody has to be asked.

Add five lines to `.env` and restart. `SMTP_USER` is a Gmail address and
`SMTP_PASSWORD` its 16-character app password, which requires 2-Step
Verification on that account (Google Account → Security → App passwords).
Google shows the app password once.

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.address@gmail.com
SMTP_PASSWORD=the16characterapppassword
SMTP_FROM=ME @ RUPP Entrance Prep <your.address@gmail.com>
```

```bash
docker compose up -d
```

```bash
curl.exe -s https://prep.your-domain.example/api/health
```

`"password_reset":true` means the sign-in screen now offers "I forgot my
password". Leave the settings out and it offers nothing, which is deliberate:
no door that leads nowhere.

**The From address is not free.** A domain's SPF record says which servers may
send as it, and `rupp.edu.kh` publishes `-all` against Microsoft's servers only
— so sending as an `@rupp.edu.kh` address through Gmail is treated as spoofing
and will be binned. Send as whichever account is authenticating. To use the
university address instead, its IT must enable **Authenticated SMTP** on that
mailbox in the Microsoft 365 admin centre; then only these five values change.

What a student sees: they enter their address, get a six-digit code by email
valid for an hour and usable once, then choose a new password. Requests are
throttled to three per address per 15 minutes so the form cannot be used to
flood somebody's inbox, a code is burned after five wrong attempts, and a
successful reset signs out every existing session on that account.

## 5c. Who has registered, and who is practising

**Teacher studio → Students** shows the roster on screen, with a CSV download.
From the command line:

```bash
docker compose exec api python tools/roster.py              # summary, then one line per student
docker compose exec api python tools/roster.py --summary    # the counts only
docker compose exec api python tools/roster.py --days 30     # change what "recently" means
docker compose exec api python tools/roster.py --csv > roster.csv
```

Read-only, and safe to run while students are working.

It reports unfinished sessions separately, which the Students screen does not
count at all. Practice has no time limit, so a student can answer twenty
questions and close the tab without ever submitting; any total built from
submitted attempts alone calls that nothing. On a launch-week roster that reads
as "nobody is practising" when the opposite may be true, so look at **sessions
still open** and **answered but not yet submitted** before drawing a
conclusion from a low completed count.

Accounts ending in `.invalid` are excluded everywhere — those are the synthetic
ones load testing and no-login workspaces create, not people.

## 6. Giving a colleague teacher access

Registration always creates a **student**, and the first teacher comes from
`TEACHER_EMAIL`. So a second colleague who needs Teacher studio has to register
normally first and then be promoted:

```bash
docker compose exec api python tools/make_teacher.py                            # list teachers
docker compose exec api python tools/make_teacher.py colleague@rupp.edu.kh
docker compose exec api python tools/make_teacher.py colleague@rupp.edu.kh --apply
```

Reversible with `--demote --apply`. Both directions are written to the audit
trail. The role is read from the account on every request, so they only reload
the page — no need to sign out.

Do this deliberately: a teacher can read every answer key, every student's
results and the whole question bank. Without it, a team sharing one studio login
also shares one audit identity, so you cannot tell who approved what.

## 7. Load-test it

```bash
docker compose exec api python tools/loadtest.py --students 250 --questions 10 --max-concurrent 100
```

That runs inside the API container, which already has `httpx`. To measure the
whole path as a browser sees it, run it from the host with
`--base http://127.0.0.1:3100`; that needs `pip install httpx` there.

**Read the last line: `failed` should be 0.** Measured on the lab stack:

```
4250 requests in 199.4s = 21 req/s, 0 failed
register p50 34ms | catalog 3ms | answer 14ms | submit 7ms
```

The defaults model a real cohort — arrivals spread over 30 s and about six
seconds of reading before each answer. Do not remove the think time to "make it
harder": without it the script asks for roughly a hundred times the concurrency
a class generates, and the result is meaningless. See
[`CAPACITY.md`](CAPACITY.md), which records that mistake being made and
corrected.

If a run does fail, check in this order:

| Check | Meaning | Fix |
|---|---|---|
| Is `--max-concurrent` above `workers × (pool + overflow)`? | The script is asking for more concurrent requests than there are connections — a request holds its connection for its whole life | Lower it, or raise `DB_POOL_SIZE` keeping `workers × (size + overflow)` below PostgreSQL's `max_connections` (300 here) |
| `QueuePool limit of size N overflow M reached` in `logs api` | Same cause, seen from the server | As above |
| Timeouts on `/api/catalog` | That endpoint touches no database, so this is never a pool problem — the client is over-driving itself | Lower `--max-concurrent`, or run the test from the host |
| Slow but zero failures | Working as intended under load | Nothing |

### Afterwards, remove the test accounts

They are `@loadtest.invalid` addresses and would otherwise clutter the Students
screen and its CSV export.

```bash
docker compose exec api python tools/remove_test_accounts.py          # reports only
docker compose exec api python tools/remove_test_accounts.py --apply
```

It refuses `@demo.local`, `@guest.invalid` and `@workspace.invalid` outright, so
it cannot take real students with it.

## 8. Before students arrive

- Serve over HTTPS with `COOKIE_SECURE=true`, or sessions will not persist.
- `PUBLIC_ORIGIN` must be the real public origin, or every write is refused.
- **Back up the `entrance-prep_data` volume** before any future migration.
- Stagger sign-up by tutorial group if you can. It is well within capacity
  either way, but a staggered start also spreads the support questions.
- **There is still no password reset.** With 250 students somebody will be locked
  out in the first week, and today the only remedy is a database edit.

## Routine operations

```bash
# who has signed up
docker compose exec api python -c "from app.models import *; from sqlalchemy import select, func; db=SessionLocal(); print(db.scalar(select(func.count()).select_from(User)))"

# logs
docker compose logs api --tail 100
docker compose logs web --tail 50

# restart after changing .env
docker compose up -d

# rebuild after a git pull
docker compose up -d --build

# back up the database
docker compose exec database pg_dump -U logic logic > backup-$(date +%F).sql
```

The Students screen in Teacher studio and its CSV export are the supported way
to read the roster; the one-liner above is only a quick count.
