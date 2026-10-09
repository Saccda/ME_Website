"""Create the mock exam that matches the real entrance examination.

The paper is 80 multiple-choice questions in 1 hour 30 minutes: 25
Mathematics, 25 Logic, 30 Physics, four options each. That is three rows, one
per section, and the sections are sat in order.

    python tools/create_exam_blueprint.py                  # report only
    python tools/create_exam_blueprint.py --apply
    python tools/create_exam_blueprint.py --apply --draft  # not yet visible

Running it again updates the paper it made before rather than adding a second
one, so it is safe to re-run after approving more questions.

It refuses to publish a paper the bank cannot fill, and says which section is
short. Three Logic sub-topics are awaiting editorial review, so Logic draws on
fewer questions than the other two sections until those are approved.
"""
import argparse
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.models import SessionLocal, Blueprint, Question, User, Audit  # noqa: E402
from sqlalchemy import select, func  # noqa: E402

NAME = "Full entrance examination · 80 questions"
MINUTES = 90
# Order matters: the rows are sat in the order written here.
ROWS = [
    {"subject": "math", "count": 25, "options": 4},
    {"subject": "logic", "count": 25, "options": 4},
    {"subject": "physics", "count": 30, "options": 4},
]


def available(db, row):
    questions = db.scalars(
        select(Question).where(Question.status == "approved",
                               Question.subject == row["subject"])
    ).all()
    return sum(1 for q in questions if len(q.content["options"]) == row["options"])


def run(apply, draft):
    with SessionLocal() as db:
        print(f"{NAME}  ·  {MINUTES} minutes  ·  {sum(r['count'] for r in ROWS)} questions\n")
        short = []
        for row in ROWS:
            have = available(db, row)
            flag = "" if have >= row["count"] else "   <-- NOT ENOUGH"
            print(f"  {row['subject']:>8}: {row['count']:>3} needed, {have:>3} approved with "
                  f"{row['options']} options{flag}")
            if have < row["count"]:
                short.append(f"{row['subject']} (needs {row['count']}, has {have})")

        existing = db.scalar(select(Blueprint).where(Blueprint.name == NAME))
        print(f"\nthis paper already exists: {'yes, it will be updated' if existing else 'no'}")

        if short and not draft:
            print("\nCannot publish yet -- short in: " + ", ".join(short))
            print("Approve more questions first, or pass --draft to save it unpublished.")
            return 1
        if not apply:
            print("\nDry run. Pass --apply to create it.")
            return 0

        teacher = db.scalar(select(User).where(User.role == "teacher"))
        if not teacher:
            print("\nNo teacher account exists, and a paper needs an author.")
            return 1

        published = not short and not draft
        if existing:
            existing.minutes, existing.rows, existing.published = MINUTES, ROWS, published
            target = existing
            action = "blueprint_updated"
        else:
            target = Blueprint(id=str(uuid.uuid4()), name=NAME, minutes=MINUTES, rows=ROWS,
                               published=published, creator_id=teacher.id)
            db.add(target)
            action = "blueprint_created"
        db.add(Audit(id=str(uuid.uuid4()), user_id=teacher.id, entity_id=target.id,
                     action=action,
                     detail={"name": NAME, "minutes": MINUTES, "rows": ROWS,
                             "published": published,
                             "note": "Matches the real paper: 25 Mathematics, 25 Logic, "
                                     "30 Physics in 90 minutes. Created from the command line."}))
        db.commit()
        print(f"\n{'Published' if published else 'Saved as a draft'}: {NAME}")
        if published:
            print("Students will find it under Mock exams.")
        else:
            print("Publish it from Teacher studio once the bank can fill every section.")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--draft", action="store_true",
                        help="Save it unpublished, even if every section could be filled.")
    args = parser.parse_args()
    raise SystemExit(run(args.apply, args.draft))
