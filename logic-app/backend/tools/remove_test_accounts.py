"""Remove the accounts a load test created, and everything they did.

The load test registers hundreds of students on @loadtest.invalid. They would
otherwise sit in the teacher's Students screen and in its CSV export, making
the real cohort hard to read. Real accounts are never matched by the default.

    python tools/remove_test_accounts.py                      # report only
    python tools/remove_test_accounts.py --apply
    python tools/remove_test_accounts.py --apply --suffix @example.com

A suffix must be given explicitly to delete anything other than the load
test's own domain, so a careless run cannot remove real students.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.models import SessionLocal, User, Attempt, AuthSession, Audit  # noqa: E402
from sqlalchemy import select, delete  # noqa: E402

PROTECTED = ("@demo.local", "@guest.invalid", "@workspace.invalid")


def run(apply, suffix):
    if any(suffix.endswith(p) for p in PROTECTED):
        raise SystemExit(f"Refusing to touch {suffix}: those are not test accounts.")
    with SessionLocal() as db:
        victims = [u for u in db.scalars(select(User)) if u.email.endswith(suffix)]
        attempts = 0
        if victims:
            ids = [u.id for u in victims]
            attempts = len(list(db.scalars(select(Attempt).where(Attempt.user_id.in_(ids[:900])))))
        print(f"accounts ending {suffix}: {len(victims)}")
        print(f"their completed and unfinished attempts: {attempts}")
        if victims[:3]:
            print("for example:", ", ".join(u.email for u in victims[:3]))
        if not apply:
            print(f"\nDry run. Pass --apply to delete {len(victims)} accounts.")
            return
        for chunk in (victims[i:i + 400] for i in range(0, len(victims), 400)):
            ids = [u.id for u in chunk]
            db.execute(delete(Attempt).where(Attempt.user_id.in_(ids)))
            db.execute(delete(AuthSession).where(AuthSession.user_id.in_(ids)))
            db.execute(delete(Audit).where(Audit.user_id.in_(ids)))
            db.execute(delete(User).where(User.id.in_(ids)))
        db.commit()
        print(f"\nDeleted {len(victims)} accounts and their attempts.")
        remaining = {}
        for u in db.scalars(select(User)):
            key = u.email.split("@")[-1]
            remaining[key] = remaining.get(key, 0) + 1
        print("accounts remaining, by address:")
        for key, n in sorted(remaining.items()):
            print(f"   @{key}: {n}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--suffix", default="@loadtest.invalid")
    args = parser.parse_args()
    run(args.apply, args.suffix)
