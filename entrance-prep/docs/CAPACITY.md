# Can it carry 250 students? — measured, not estimated

Written 2026-10-03, after you said roughly 250 students will use the platform
once it is deployed.

## How it was measured

A script simulates a cohort arriving at once. Each simulated student does the
real sequence, writes included: register → load the workspace (catalogue,
availability, attempts, analytics in parallel, as the browser does) → start a
10-question practice set → answer all ten → submit. Run against the local stack
through the Next proxy, which is the same path a browser takes.

This is the worst case on purpose: every student arrives in the same second. A
class told "sign up now" behaves exactly like this.

## What it found, before any fix

| Cohort | Result |
|---|---|
| 250 students | **836 of 1522 requests failed (55%)**, 4 req/s, registration median **26 s** |

The log gave the cause exactly:

```
sqlalchemy.exc.TimeoutError: QueuePool limit of size 5 overflow 10 reached,
connection timed out, timeout 30.00
```

**Two independent faults, both now fixed:**

1. **The connection pool was eight times too small for the thread pool.** The
   engine used SQLAlchemy's defaults — 5 connections plus 10 overflow — while
   FastAPI runs synchronous endpoints on a 40-thread pool. Forty threads
   competed for fifteen connections; the losers waited 30 seconds and returned
   500. Nothing about this is visible at low load.

2. **Threads outnumbered connections, so load turned into errors rather than a
   queue.** A request would take a thread, then fail waiting for a connection it
   could never get. The thread pool is now matched to the connection pool, so a
   busy server makes people wait instead of failing them.

Password hashing was suspected and cleared by measurement: scrypt costs 35 ms
and runs 266/s across threads, so 250 students cost about one second. It is not
the bottleneck, and its cost should not be reduced.

## After the fix

| Cohort | Failures | Throughput | Registration median |
|---|---|---|---|
| 40 students | **0 of 680** | **86 req/s** | 2.9 s |
| 100 students | 443 of 600 | 6 req/s | 6.7 s (registration itself passed) |
| 250 students | still fails | — | — |

40 concurrent students went from **100% failure at 1 req/s** to **zero failures
at 86 req/s**.

## The remaining limit is SQLite, and production does not use it

Above roughly 40 simultaneous students the local stack still fails, and the
reason is SQLite: it permits **one writer at a time**. Every student action here
is a write — registering, opening a session, saving an answer, submitting — so
writers queue, each holding its connection while it waits.

**`docker-compose.yml` already uses PostgreSQL 17**, which does not serialise
writers this way, applies migrations on start, and sets `COOKIE_SECURE`. So the
production path is the right one and the SQLite ceiling does not apply to it.

**What is therefore still unproven:** I could not load-test PostgreSQL, because
Docker Desktop was not running on this machine. The fixes above are engine
independent and will help there too, but **the 250-student run must be repeated
against the Compose stack before you open it to students.** Do not take the
"40 students" figure as the platform's capacity — take it as proof of the fault
that was fixed.

Do not deploy this on SQLite. The ME website's lab backend uses SQLite; if this
app is deployed the same way, it will fail with a class of this size.

## Two blockers found in the deployment file

Both would have stopped a sign-up launch, and both are now fixed in
`docker-compose.yml`:

1. **`AUTH_MODE: open`.** There would have been no sign-up at all, and Teacher
   studio — every answer key — would have been reachable by any visitor.
2. **No `TEACHER_EMAIL` / `TEACHER_PASSWORD`.** With `AUTH_MODE` not "open" and
   `DEMO_MODE: false`, the API **refuses to start**: it raises rather than come
   up with no way to review or approve anything. The deployment would simply not
   have booted.

Pool sizes are now settable per deployment. Keep
`(DB_POOL_SIZE + DB_MAX_OVERFLOW) × api replicas` below PostgreSQL's
`max_connections`, which defaults to 100.

## Update, 2026-10-08: measured on the lab stack, and fixed

The 250-student run on PostgreSQL **registered all 250 successfully** — the pool
and thread-pool fix above worked — and then failed all four workspace calls:
1000 of 1500 requests failed, 12 req/s. One detail gave away the cause:
`/api/catalog`, which touches no database at all, recorded a **30-second**
maximum. A trivial endpoint can only be that slow if it is queued behind
saturated ones.

Reproduced locally. Each endpoint on its own is fast — catalog 0.9 ms,
availability 6.4 ms, attempts 1.4 ms, analytics 1.4 ms — so there is no slow
query. The limit is that **every request holds its database connection for its
whole life**, which makes one worker's concurrency equal to its pool size:

| Pool | Workspace burst served | Collapsed at |
|---|---|---|
| 30 (the shipped default) | 25 students / 100 calls, 181 req/s | 60 students |
| 120 | 60 students / 240 calls, 186 req/s | 150 students |

The browser makes four calls on load, so 250 students is 1000 concurrent
requests. No pool size reaches that on a single core — and a saturated single
worker did not recover, still timing out minutes later.

**Four workers settle it**, measured on the same machine:

| 150 students, 600 calls | Time | Throughput | Failed |
|---|---|---|---|
| 1 worker | 32.6 s | 18 req/s | 78 |
| 4 workers | 2.7 s | **221 req/s** | **0** |

At 250 students the burst served 952 calls at **378 req/s with no failures**, and
the full journey — register, load, ten answers, submit — completed 4202 requests
with 3 failures, all in registration, where SQLite serialises its two commits.
PostgreSQL does not share that limit.

Shipped as a result: `WEB_CONCURRENCY` (4 by default in compose),
`DB_POOL_SIZE` 50 and `DB_MAX_OVERFLOW` 20, PostgreSQL started with
`max_connections=300`, and startup seeding wrapped in a PostgreSQL advisory
lock so several workers can start without double-seeding the bank.

Keep `workers × (pool + overflow)` below `max_connections`.

## Correction, 2026-10-08: the platform carries 250 students comfortably

The alarming numbers above, and in the lab runs, came from a test that did not
model students. Two faults in the script, both mine:

1. **No think time.** It fired each student's eleven requests back to back.
   A real student spends seconds reading a question, so this asked for roughly a
   hundred times the concurrency a class generates.
2. **One HTTP client per student, all open at once.** 250 clients holding up to
   1000 sockets made the script the bottleneck. The giveaway was `/api/catalog`
   timing out — an endpoint that touches no database and cannot be affected by
   pool size.

With both corrected — arrivals spread over 30 s, 3 s of reading per question,
and client concurrency held below the pool — the measured result on **one worker
with the shipped default pool of 30** is:

| 250 students, 5 questions each | |
|---|---|
| Requests | **3,000** |
| Failed | **0** |
| Throughput | 18 req/s |
| register | p50 52 ms |
| availability | p50 18 ms |
| answer | p50 8 ms |
| submit | p50 5 ms |

**So 250 students practising is well within capacity**, and the four workers now
shipped give roughly nine times that headroom.

The honest model: the server serves requests quickly while **concurrent
in-flight requests stay below `workers × (pool + overflow)`**, because each
request holds its connection for its whole life. Above that, requests queue,
hit the 30 s pool timeout and turn into 500s. With realistic reading time, 250
students never come close to that line.

What remains true from the earlier sections: the pool default of 5 + 10 was
genuinely too small and is fixed; SQLite genuinely serialises writes and should
not be used for a cohort; and a *simultaneous* burst of 1000 requests would
still exceed one worker, which is why four are now configured.

## Confirmed on the lab stack, 2026-10-08

The corrected test, run against the real deployment — PostgreSQL, four workers,
250 students answering ten questions each, up to a hundred in flight:

```
step            calls  fail   p50 ms   p95 ms   max ms
--------------------------------------------------------
register          250     0       34       46       78
catalog           250     0        3        5       62
analytics         250     0        8       20       38
attempts          250     0        8       20       64
availability      250     0       14       29       70
start attempt     250     0       10       19       66
answer           2500     0       14       23       41
submit            250     0        7       11       20

4250 requests in 199.4s = 21 req/s, 0 failed
```

Zero failures on every step, and nothing above 78 ms at the median. **The
capacity question is settled.** 21 req/s is what a cohort of this size actually
generates when its members read the questions; it is not a ceiling.

## Still worth doing before the 250 arrive

1. **Use a registration code rather than a rate limit.** A real cohort signing
   up together is indistinguishable from an attack; a code admits the class and
   excludes everyone else. Not built — see `ROADMAP.md`.
2. **Stagger sign-up if you can** — by tutorial group rather than all at once.
   Not for capacity, which is fine, but to spread the support questions.
3. **Back up the `logic-data` volume** before any future migration.

## How to repeat this measurement

```bash
docker compose exec api python tools/loadtest.py --students 250 --questions 10 --max-concurrent 100
docker compose exec api python tools/remove_test_accounts.py --apply
```

Keep the think time. Removing it does not make the test stricter, it makes it
meaningless — that is the whole lesson of the correction above.
