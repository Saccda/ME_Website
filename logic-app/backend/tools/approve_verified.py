"""Approve the questions whose answers a machine has proved.

A fresh non-demo installation seeds every question as a draft, so students see
"0 approved questions match" until a teacher approves them one at a time. That
is the correct default -- nothing reaches a student unreviewed -- but it leaves
nothing to practise on launch day.

This approves only the questions whose validation method is `deterministic`,
meaning the server recomputed the answer from the question's declared rule and
it agreed with the key. Questions validated `editorial` are never touched: no
machine checked those, and they are exactly the ones a teacher must read.

What this does NOT certify, and what a teacher should still skim for: that the
wording is unambiguous, that the distractors are plausible, and that the topic
and difficulty labels are fair. A deterministic proof covers the arithmetic and
the key, not the English.

    python tools/approve_verified.py                      # report only
    python tools/approve_verified.py --apply
    python tools/approve_verified.py --apply --subject math
"""
import argparse
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.models import SessionLocal, Question, User, Audit  # noqa: E402
from app.validation import validate  # noqa: E402
from sqlalchemy import select  # noqa: E402


def run(apply, subject=None):
    with SessionLocal() as db:
        teacher = db.scalar(select(User).where(User.role == "teacher"))
        if not teacher:
            raise SystemExit("No teacher account exists. Start the application first.")

        query = select(Question).where(Question.status.in_(("draft", "review")))
        if subject:
            query = query.where(Question.subject == subject)
        pending = list(db.scalars(query))

        proved, editorial, disagreed = [], [], []
        for q in pending:
            method = (q.validation or {}).get("method")
            if method != "deterministic":
                editorial.append(q)
                continue
            # Re-check now rather than trusting the stored verdict.
            fresh = validate(q.content)
            if fresh["passed"] and fresh["method"] == "deterministic":
                proved.append(q)
            else:
                disagreed.append((q, fresh.get("errors")))

        by_subject = {}
        for q in proved:
            by_subject[q.subject] = by_subject.get(q.subject, 0) + 1

        print(f"pending questions            : {len(pending)}")
        print(f"  answer proved by recompute : {len(proved)}  {json.dumps(by_subject)}")
        print(f"  editorial, left for review : {len(editorial)}")
        print(f"  proof disagreed, left alone: {len(disagreed)}")
        for q, errors in disagreed[:5]:
            print(f"      {q.subject}/{q.domain}/{q.difficulty}: {errors}")

        if not apply:
            print(f"\nDry run. Pass --apply to approve {len(proved)} questions.")
            return

        for q in proved:
            q.status = "approved"
            db.add(Audit(
                id=str(uuid.uuid4()), user_id=teacher.id, entity_id=q.id,
                action="approved_machine_proved",
                detail={"version": q.version, "method": "deterministic",
                        "proof": (q.validation or {}).get("proof"),
                        "note": "Answer recomputed from the declared rule and it agreed "
                                "with the key. Wording, distractors and labelling were "
                                "not reviewed by a person."},
            ))
        db.commit()
        print(f"\nApproved {len(proved)} questions.")
        print(f"{len(editorial)} still need a teacher to read them before students see them.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--subject")
    args = parser.parse_args()
    run(args.apply, args.subject)
