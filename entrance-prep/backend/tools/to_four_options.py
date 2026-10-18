"""Bring existing five-option questions down to the paper's four.

The entrance examination offers four choices, so the platform should too: a
student practising five-option questions is rehearsing a shape they will never
sit, and the odds of a lucky guess differ from the real thing.

New questions are seeded at four options, but the seeder only fills a sub-topic
that is empty, so it never revisits a database that already holds five-option
questions. This does.

    python tools/to_four_options.py          # report only
    python tools/to_four_options.py --apply

One distractor is removed -- the last option that is not the answer -- and the
four that remain are shuffled and re-lettered A to D. The stem, the answer and
the worked explanation are untouched, so the question still asks and teaches
the same thing with one fewer wrong choice.

The shuffle is not decoration. Removing the last wrong option and keeping the
order meant that every question whose answer had been E came out with its
answer at D, and a measured run put 39% of converted answers on D against the
25% chance deserves. Position would then carry information, which is the same
defect the examination panel's own bank had. The shuffle is seeded from the
question id, so running this twice gives the same arrangement.

Each change bumps the question's version and is recorded in the audit trail, and
every converted question is re-validated before it is written: a question that
would no longer pass is left alone and reported, rather than being quietly
degraded.

Attempts already sat are unaffected. An attempt stores its own snapshot of each
question, so a paper a student is part-way through keeps the five options it
was served, and a finished attempt still shows what was actually asked.
"""
import argparse
import random
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sqlalchemy import select  # noqa: E402
from app.models import SessionLocal, Question, User, Audit  # noqa: E402
from app.validation import validate  # noqa: E402


def shrink(content, seed):
    """The same question with its last wrong option removed, then shuffled."""
    options = content["options"]
    correct = content["correct"]
    victim = next((o for o in reversed(options) if o["id"] != correct), None)
    if victim is None:
        return None
    kept = [o for o in options if o is not victim]
    random.Random(seed).shuffle(kept)
    relettered = [{**o, "id": "ABCDE"[i]} for i, o in enumerate(kept)]
    # The answer keeps its text, so find where it landed after re-lettering.
    answer = next(o["text"] for o in options if o["id"] == correct)
    new_correct = next(o["id"] for o in relettered if o["text"] == answer)
    return {**content, "options": relettered, "correct": new_correct}


def run(apply):
    with SessionLocal() as db:
        oversized = [q for q in db.scalars(select(Question))
                     if len(q.content.get("options", [])) > 4]
        print(f"questions with more than four options: {len(oversized)}")
        if not oversized:
            print("Nothing to do.")
            return 0

        by_subject = {}
        for q in oversized:
            by_subject[q.subject] = by_subject.get(q.subject, 0) + 1
        for subject, n in sorted(by_subject.items()):
            print(f"  {subject:>8}: {n}")

        planned, refused = [], []
        for q in oversized:
            content = shrink(q.content, q.id)
            if content is None:
                refused.append((q.id, "no option to remove"))
                continue
            report = validate(content)
            if not report["passed"]:
                refused.append((q.id, "; ".join(report["errors"])))
                continue
            planned.append((q, content, report))

        print(f"\n  convertible : {len(planned)}")
        print(f"  left alone  : {len(refused)}")
        for qid, why in refused[:10]:
            print(f"    {qid}: {why}")

        if not apply:
            print("\nDry run. Pass --apply to convert them.")
            return 0

        teacher = db.scalar(select(User).where(User.role == "teacher"))
        if not teacher:
            print("\nNo teacher account exists, and a change needs an author for its audit.")
            return 1

        for q, content, report in planned:
            db.add(Audit(id=str(uuid.uuid4()), user_id=teacher.id, entity_id=q.id,
                         action="reduced_to_four_options",
                         detail={"version": q.version + 1,
                                 "removed": next(o["text"] for o in q.content["options"]
                                                 if o["text"] not in
                                                 {k["text"] for k in content["options"]}),
                                 "previous_correct": q.content["correct"],
                                 "correct": content["correct"],
                                 "note": "The entrance paper offers four choices; the answer "
                                         "and the stem are unchanged."}))
            q.content = content
            q.validation = report
            q.version += 1
        db.commit()
        print(f"\nConverted {len(planned)} questions to four options.")
        if refused:
            print(f"{len(refused)} were left as they were; see above.")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    raise SystemExit(run(args.apply))
