"""Simulate a cohort of students using the platform.

Each simulated student does the real sequence, writes included: register, load
the workspace (four calls at once, as the browser does), start a practice set,
answer every question, submit. Accounts are created on @loadtest.invalid so
they can be identified and removed afterwards.

    python tools/loadtest.py --help
    python tools/loadtest.py --students 250 --ramp 60
    python tools/loadtest.py --students 250 --base http://127.0.0.1:3100

Never run this against a database holding real student work: it registers
hundreds of accounts and submits hundreds of attempts.

READING THE RESULT. The last line is what matters, and `failed` should be 0.

The defaults model a real cohort, because the first versions of this script did
not and the results were alarming nonsense. Two mistakes are worth knowing
about, since both are easy to repeat:

1. No think time. Firing a student's eleven requests back to back asks for
   roughly a hundred times the concurrency a real class generates, because a
   real student spends seconds reading each question. With --think, 250 students
   measured 18 req/s and no failures on a single worker; without it, the same
   250 appeared to collapse the server.

2. One client per student, all open at once. 250 clients holding up to 1000
   sockets made this script, not the server, the bottleneck -- including
   timeouts on /api/catalog, which touches no database at all. --max-concurrent
   bounds that. Container `ulimit -n` is often 1024.

So a failing run means one of three things, in this order of likelihood: the
script is over-driving itself, --max-concurrent is above the server's pool
capacity, or the server really is out of capacity. Check them in that order.
"""
import argparse
import asyncio
import random
import statistics
import sys
import time

try:
    import httpx
except ImportError:
    raise SystemExit("pip install httpx, or run inside the backend virtualenv.")

parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
parser.add_argument("--students", type=int, default=250)
parser.add_argument("--questions", type=int, default=10)
parser.add_argument("--base", default="http://127.0.0.1:8000",
                    help="Address to test. The API directly, or the web port as a browser sees it.")
parser.add_argument("--origin", default=None,
                    help="Send this as the Origin header, to exercise the write guard too. "
                         "Must be a value in APP_ORIGINS. Omitted by default, which the guard "
                         "allows, because the address under test is usually not the site's origin.")
parser.add_argument("--ramp", type=float, default=30,
                    help="Spread student arrivals over this many seconds. 0 is an instantaneous burst.")
parser.add_argument("--max-concurrent", type=int, default=25,
                    help="How many students may be in flight at once. Keep it below "
                         "workers x (DB_POOL_SIZE + DB_MAX_OVERFLOW): a request holds its "
                         "connection for its whole life, so above that requests queue, hit "
                         "the pool timeout and become 500s. Raise it to find the ceiling.")
parser.add_argument("--think", type=float, default=6,
                    help="Average seconds a student spends reading before each answer. "
                         "0 answers as fast as the machine can, which no student does and "
                         "which demands far more concurrency than a real cohort.")
args = parser.parse_args()

BASE = args.base.rstrip("/")
HEADERS = {"X-App-Request": "1", "Content-Type": "application/json"}
if args.origin:
    HEADERS["Origin"] = args.origin.rstrip("/")

timings, failures = {}, {}
stamp = int(time.time())


async def call(client, label, method, path, json=None):
    started = time.perf_counter()
    try:
        r = await client.request(method, BASE + path, json=json, headers=HEADERS, timeout=60)
        if r.status_code >= 400:
            failures.setdefault(label, []).append(f"{r.status_code} {r.text[:90]}")
        timings.setdefault(label, []).append(time.perf_counter() - started)
        return r
    except Exception as e:
        timings.setdefault(label, []).append(time.perf_counter() - started)
        failures.setdefault(label, []).append(f"{type(e).__name__}: {e}")
        return None


async def student(n, gate):
    if args.ramp:
        await asyncio.sleep(random.uniform(0, args.ramp))
    async with gate:
        async with httpx.AsyncClient() as client:
            r = await call(client, "register", "POST", "/api/auth/register", {
                "name": f"Load Student {n}",
                "email": f"load-{stamp}-{n}@loadtest.invalid",
                "password": "practice-logic-2026",
            })
            if r is None or r.status_code >= 400:
                return
            await asyncio.gather(
                call(client, "catalog", "GET", "/api/catalog"),
                call(client, "availability", "GET", "/api/availability"),
                call(client, "attempts", "GET", "/api/attempts"),
                call(client, "analytics", "GET", "/api/analytics"),
            )
            r = await call(client, "start attempt", "POST", "/api/attempts", {
                "mode": "practice", "count": args.questions, "options": 4,
            })
            if r is None or r.status_code >= 400:
                return
            attempt = r.json()
            for q in attempt["questions"]:
                if args.think:
                    # A student reads the question before answering. Without this
                    # the test asks for concurrency no real cohort generates.
                    await asyncio.sleep(random.uniform(args.think * 0.5, args.think * 1.5))
                await call(client, "answer", "POST", f"/api/attempts/{attempt['id']}/answer",
                           {"question_id": q["id"], "option_id": q["content"]["options"][0]["id"]})
            await call(client, "submit", "POST", f"/api/attempts/{attempt['id']}/submit")


async def main():
    shape = "all at once" if not args.ramp else f"arriving over {args.ramp:g}s"
    print(f"{args.students} students x {args.questions} questions against {BASE}, {shape}, "
          f"at most {args.max_concurrent} in flight\n")
    if args.think:
        print(f"  each student pauses about {args.think:g}s before every answer, as a reader does")
    gate = asyncio.Semaphore(args.max_concurrent)
    began = time.perf_counter()
    await asyncio.gather(*(student(i, gate) for i in range(args.students)))
    elapsed = time.perf_counter() - began

    total = sum(len(v) for v in timings.values())
    bad = sum(len(v) for v in failures.values())
    print(f"{'step':14} {'calls':>6} {'fail':>5} {'p50 ms':>8} {'p95 ms':>8} {'max ms':>8}")
    print("-" * 56)
    for label, values in timings.items():
        values = sorted(values)
        p95 = values[min(len(values) - 1, int(len(values) * 0.95))]
        print(f"{label:14} {len(values):>6} {len(failures.get(label, [])):>5}"
              f" {statistics.median(values)*1000:>8.0f} {p95*1000:>8.0f} {values[-1]*1000:>8.0f}")
    print(f"\n{total} requests in {elapsed:.1f}s = {total/elapsed:.0f} req/s, {bad} failed")
    for label, details in failures.items():
        seen = {}
        for d in details:
            seen[d[:70]] = seen.get(d[:70], 0) + 1
        print(f"\n  {label} failures:")
        for text, count in sorted(seen.items(), key=lambda x: -x[1])[:4]:
            print(f"    x{count}  {text}")
    print("\nRemove the test accounts afterwards: they are the @loadtest.invalid addresses.")
    return 1 if bad else 0


sys.exit(asyncio.run(main()))
