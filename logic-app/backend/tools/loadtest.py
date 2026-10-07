"""Simulate a cohort of students arriving at once.

Each simulated student does the real sequence, writes included: register, load
the workspace (four calls in parallel, as the browser does), start a practice
set, answer every question, submit. Accounts are created on @loadtest.invalid
so they can be identified and removed afterwards.

    python tools/loadtest.py                                  # 250 students, local
    python tools/loadtest.py 250 10 http://127.0.0.1:3000     # explicit
    python tools/loadtest.py 50 10 https://logic.example.edu

Never run this against a database holding real student work: it registers
hundreds of accounts and submits hundreds of attempts.

What to look for: the "failed" count should be zero. Non-zero means the stack
could not carry the cohort. A pool timeout in the API log means the database
pool is smaller than the request thread pool (see DB_POOL_SIZE).
"""
import asyncio
import statistics
import sys
import time

try:
    import httpx
except ImportError:
    raise SystemExit("pip install httpx, or run inside the backend virtualenv.")

STUDENTS = int(sys.argv[1]) if len(sys.argv) > 1 else 250
QUESTIONS = int(sys.argv[2]) if len(sys.argv) > 2 else 10
BASE = (sys.argv[3] if len(sys.argv) > 3 else "http://127.0.0.1:3000").rstrip("/")
# The write guard checks the browser origin, which is the site's own.
HEADERS = {"X-App-Request": "1", "Origin": BASE, "Content-Type": "application/json"}

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


async def student(n):
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
            "mode": "practice", "count": QUESTIONS, "options": 4,
        })
        if r is None or r.status_code >= 400:
            return
        attempt = r.json()
        for q in attempt["questions"]:
            await call(client, "answer", "POST", f"/api/attempts/{attempt['id']}/answer",
                       {"question_id": q["id"], "option_id": q["content"]["options"][0]["id"]})
        await call(client, "submit", "POST", f"/api/attempts/{attempt['id']}/submit")


async def main():
    print(f"simulating {STUDENTS} students x {QUESTIONS} questions against {BASE}\n")
    began = time.perf_counter()
    await asyncio.gather(*(student(i) for i in range(STUDENTS)))
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


asyncio.run(main())
