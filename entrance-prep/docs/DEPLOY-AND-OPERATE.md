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

The Compose project name is now pinned to `logic-studio` inside
`docker-compose.yml`, which is the name your existing database volume is
attached to. So the stack comes back up on the same data, and `-p logic-studio`
is no longer needed on the command line — though passing it does no harm.

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
migrated for you (currently through `0003`). Startup seeding is wrapped in a
PostgreSQL advisory lock, so the four workers cannot seed the bank twice.

Confirm the workers actually started — `logs api` should show four
`Started server process` lines.

## 4. Approve something to practise — do not skip this

A fresh installation seeds **252 questions, none approved**. That is the correct
default, since nothing should reach a student unreviewed, but on launch day a
student would otherwise get

> Only 0 approved questions match. Reduce the count or broaden your filters.

```bash
docker compose exec api python tools/approve_verified.py          # reports only
docker compose exec api python tools/approve_verified.py --apply
```

Measured result: **216 approved** (84 Mathematics, 84 Physics, 48 Logic), **36
left as drafts**. The 36 are the `editorial` ones — verbal and argument
reasoning, where no machine can prove an answer — and they are exactly the
questions a teacher must read. They stay invisible to students until approved in
Question bank, and until then those three Logic sub-topics show as "none
approved yet" and cannot be selected.

The tool certifies that the server recomputed each answer from the question's
declared rule and it matched the key. It does **not** certify that the wording is
unambiguous, the distractors plausible, or the difficulty label fair. Every
approval is recorded in the audit trail as `approved_machine_proved` with that
caveat.

## 5. The mock exam that matches the real paper

80 questions in 90 minutes — 25 Mathematics, 25 Logic, 30 Physics, four options
each, sat in that order. One command builds it:

```bash
docker compose exec api python tools/create_exam_blueprint.py          # reports only
docker compose exec api python tools/create_exam_blueprint.py --apply
```

It refuses to publish a paper the bank cannot fill and names the short section.
Re-running updates the paper it made before rather than adding a second one, so
it is safe to run again after approving more questions. `--draft` saves it
unpublished if you want to look before students can.

Students find it under **Mock exams**. On submission they get a score per
section — Mathematics 18 / 25, Logic 20 / 25, Physics 22 / 30 — the way the real
paper is marked, as well as the total.

Teacher studio can build other papers the same way: a blueprint row may name a
whole subject, or a single sub-topic and level as rows always could.

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
- **Back up the `logic-data` volume** before any future migration.
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
