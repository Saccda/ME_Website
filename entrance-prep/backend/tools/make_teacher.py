"""Grant or withdraw teacher access for an account that already exists.

A role is set once and never changes: registration always creates a student,
and the first teacher comes from TEACHER_EMAIL at startup. So a second
colleague who needs Teacher studio has no way in without this.

    python tools/make_teacher.py                              # list teachers
    python tools/make_teacher.py colleague@rupp.edu.kh
    python tools/make_teacher.py colleague@rupp.edu.kh --apply
    python tools/make_teacher.py colleague@rupp.edu.kh --demote --apply

The account must already exist, so the colleague registers normally first and
is then promoted. Nothing here creates an account or sets a password, and the
password is untouched by a role change.

A teacher can read every answer key, every student's results, and the whole
question bank. Promote deliberately: --apply is required, and every change is
written to the audit trail as role_granted or role_withdrawn.
"""
import argparse
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.models import SessionLocal, User, Audit  # noqa: E402
from sqlalchemy import select  # noqa: E402


def show_teachers(db):
    teachers = list(db.scalars(select(User).where(User.role == "teacher").order_by(User.email)))
    print(f"teachers ({len(teachers)}):")
    for t in teachers:
        print(f"   {t.email}  --  {t.name}")
    if not teachers:
        print("   none, which means nobody can review or approve a question")
    return teachers


def run(email, apply, demote):
    with SessionLocal() as db:
        if not email:
            show_teachers(db)
            print("\nPass an email address to grant or withdraw access.")
            return 0

        email = email.lower().strip()
        user = db.scalar(select(User).where(User.email == email))
        if not user:
            print(f"No account for {email}.")
            print("They register at the site first, then run this to promote them.")
            return 1

        wanted = "student" if demote else "teacher"
        verb = "Withdrawing teacher access from" if demote else "Granting teacher access to"
        if user.role == wanted:
            print(f"{email} is already {wanted}. Nothing to do.")
            return 0

        print(f"{verb} {email} ({user.name}), currently {user.role}.")
        if not demote:
            print("That grants every answer key, every student's results, and the question bank.")
        if not apply:
            print("\nDry run. Pass --apply to make the change.")
            return 0

        was = user.role
        user.role = wanted
        db.add(Audit(
            id=str(uuid.uuid4()), user_id=user.id, entity_id=user.id,
            action="role_withdrawn" if demote else "role_granted",
            detail={"from": was, "to": wanted,
                    "note": "Changed from the command line by an operator with database access."},
        ))
        db.commit()
        # The role is read from this row on every request, not cached in the
        # session, so there is no need to sign out -- but the browser holds the
        # old role in its own state until the page is reloaded.
        print(f"\n{email} is now {wanted}. They reload the page to see it.\n")
        show_teachers(db)
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("email", nargs="?", help="The account to change. Omit to list current teachers.")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--demote", action="store_true", help="Return the account to student.")
    args = parser.parse_args()
    raise SystemExit(run(args.email, args.apply, args.demote))
