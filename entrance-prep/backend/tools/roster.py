"""Who has registered, and who is actually practising.

    python tools/roster.py              # summary, then one line per student
    python tools/roster.py --summary    # the counts only
    python tools/roster.py --csv        # CSV on stdout, to redirect to a file
    python tools/roster.py --days 30    # change what "recently" means

Read-only. Safe to run while students are using the platform.

It counts unfinished work, which the Students screen does not. Practice has no
time limit, so a student who answers twenty questions and closes the tab never
submits, and every total built from submitted attempts alone reports them as
having done nothing. On a roster that is read as "nobody is practising" when
the truth may be the opposite, so sessions in progress are counted and shown
separately rather than folded in or left out.

Accounts ending in ".invalid" are excluded throughout: those are the synthetic
ones that load testing and no-login workspaces create, not people.
"""
import argparse
import csv
import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sqlalchemy import select  # noqa: E402
from app.models import SessionLocal, User, Attempt, now  # noqa: E402
from app.security import utc  # noqa: E402

HEADER = ["Name", "Email", "Registered", "Completed", "In progress",
          "Answered", "Correct", "Accuracy %", "Last active"]


def gather(db, days):
    cutoff = now() - timedelta(days=days)
    students = [u for u in db.scalars(select(User).where(User.role == "student"))
                if not u.email.lower().endswith(".invalid")]
    known = {u.id for u in students}
    done, open_now = {}, {}
    for a in db.scalars(select(Attempt)):
        if a.user_id not in known:
            continue
        (done if a.submitted else open_now).setdefault(a.user_id, []).append(a)

    rows = []
    for u in sorted(students, key=lambda x: x.name.lower()):
        finished = done.get(u.id, [])
        answered = correct = 0
        for a in finished:
            for q in a.snapshots:
                answered += 1
                correct += int(a.answers.get(q["id"]) == q["content"]["correct"])
        # Answers given inside a session that was never submitted still show
        # someone working; they are reported on their own, not added above.
        unsubmitted = sum(len(a.answers) for a in open_now.get(u.id, []))
        last = max([utc(a.submitted) for a in finished]
                   + [utc(a.started) for a in open_now.get(u.id, [])], default=None)
        rows.append({
            "name": u.name, "email": u.email,
            "registered": utc(u.created).date().isoformat() if u.created else "",
            "completed": len(finished), "in_progress": len(open_now.get(u.id, [])),
            "answered": answered, "correct": correct,
            "accuracy": round(correct / answered * 100) if answered else None,
            "last_active": last,
            "unsubmitted_answers": unsubmitted,
            "new": bool(u.created and utc(u.created) > cutoff),
            "recent": bool(last and last > cutoff),
        })
    return rows


def summarise(rows, days):
    """Counts, with the labels padded to whatever the longest one turns out to
    be -- "last {days} days" changes width with the argument, so a fixed pad
    leaves the colons ragged."""
    touched = [r for r in rows if r["completed"] or r["in_progress"]]
    unsub = sum(r["unsubmitted_answers"] for r in rows)
    graded = [r for r in rows if r["accuracy"] is not None]
    lines = [
        ("registered students", len(rows)),
        (f"  signed up in the last {days} days", sum(r["new"] for r in rows)),
        ("  have started practising", len(touched)),
        (f"  active in the last {days} days", sum(r["recent"] for r in rows)),
        ("  registered, never started", len(rows) - len(touched)),
        (None, None),
        ("completed sessions", sum(r["completed"] for r in rows)),
        ("sessions still open", sum(r["in_progress"] for r in rows)),
        ("questions answered", sum(r["answered"] for r in rows)),
    ]
    if unsub:
        lines.append(("  answered but not yet submitted", unsub))
    if graded:
        overall = sum(r["correct"] for r in graded) / sum(r["answered"] for r in graded)
        lines.append(("accuracy across all marked work", f"{overall*100:.0f}%"))
    width = max(len(label) for label, _ in lines if label)
    for label, value in lines:
        print("" if label is None else f"{label:<{width}} : {value}")


def main(args):
    with SessionLocal() as db:
        rows = gather(db, args.days)

    if args.csv:
        writer = csv.writer(sys.stdout, lineterminator="\n")
        writer.writerow(HEADER)
        for r in rows:
            writer.writerow([r["name"], r["email"], r["registered"], r["completed"],
                             r["in_progress"], r["answered"], r["correct"],
                             "" if r["accuracy"] is None else r["accuracy"],
                             r["last_active"].date().isoformat() if r["last_active"] else ""])
        return 0

    if not rows:
        print("No students have registered yet.")
        return 0

    summarise(rows, args.days)
    if args.summary:
        return 0

    print()
    print(f"{'name':<22} {'registered':<11} {'done':>4} {'open':>4} "
          f"{'answered':>8} {'acc':>4}  last active")
    print("-" * 78)
    for r in rows:
        acc = "" if r["accuracy"] is None else f"{r['accuracy']}%"
        last = r["last_active"].date().isoformat() if r["last_active"] else "never"
        print(f"{r['name'][:22]:<22} {r['registered']:<11} {r['completed']:>4} "
              f"{r['in_progress']:>4} {r['answered']:>8} {acc:>4}  {last}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", action="store_true", help="Counts only, no per-student list.")
    parser.add_argument("--csv", action="store_true", help="CSV on stdout.")
    parser.add_argument("--days", type=int, default=7, help='What "recently" means. Default 7.')
    raise SystemExit(main(parser.parse_args()))
