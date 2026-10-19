"""Bring an over-full bank down to the weighted targets.

Seeding only ever adds, so lowering a target stops growth without shrinking
what is already there. An installation seeded under the old flat target holds
far more than the examination's shape justifies -- 812 Physics questions spread
evenly over sub-topics worth between 1 and 15 marks.

    python tools/prune_to_target.py          # report only
    python tools/prune_to_target.py --apply
    python tools/prune_to_target.py --apply --subject physics

Imported questions are never touched: the panel's own bank is not generated
practice and is not what any target describes.

Which questions go, when a slot is over its target: the ones no student has
ever been served, newest first. A question that has appeared in somebody's
attempt has a place in the per-question report, and discarding it would quietly
rewrite what that report is built from. If a slot is still over target once the
unserved ones are gone, it is left over target and said so, rather than
reaching into work students have done.

Deleting a question does not disturb attempts already sat. Each attempt stores
its own snapshot of every question it served, so a finished paper still shows
exactly what was asked, and the per-question report already marks a question it
can no longer find as "deleted".
"""
import argparse
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sqlalchemy import select  # noqa: E402
from app.catalog import DOMAINS, LEVELS, GENERATED_SUBJECTS, EXAM_WEIGHTS  # noqa: E402
from app.main import slot_target, EDITORIAL_PER_SLOT  # noqa: E402
from app.models import SessionLocal, Question, Attempt, User, Audit  # noqa: E402


def served_counts(db):
    """How many times each question has been put in front of a student."""
    counts = {}
    for a in db.scalars(select(Attempt)):
        for q in a.snapshots:
            counts[q["id"]] = counts.get(q["id"], 0) + 1
    return counts


def plan(db, subject):
    served = served_counts(db)
    generated = [q for q in db.scalars(select(Question)) if not q.source.get("kind")]
    slots = {}
    for q in generated:
        slots.setdefault((q.domain, q.difficulty), []).append(q)

    rows = []
    for d in DOMAINS:
        if subject and d["subject"] != subject:
            continue
        for level in LEVELS:
            group = slots.get((d["id"], level), [])
            target = slot_target(d["id"])
            if group and any((q.validation or {}).get("method") != "deterministic" for q in group):
                target = min(target, EDITORIAL_PER_SLOT)
            excess = len(group) - target
            if excess <= 0:
                continue
            # Unserved first, and within those the newest, so the bank keeps
            # the questions that have been around long enough to be trusted.
            spare = sorted((q for q in group if not served.get(q.id)),
                           key=lambda q: q.created, reverse=True)
            rows.append({"domain": d["id"], "subject": d["subject"], "level": level,
                         "have": len(group), "target": target, "excess": excess,
                         "removable": spare[:excess],
                         "protected": max(0, excess - len(spare))})
    return rows


def run(apply, subject):
    with SessionLocal() as db:
        rows = plan(db, subject)
        generated = [q for q in db.scalars(select(Question)) if not q.source.get("kind")]
        by_subject = {}
        for q in generated:
            by_subject[q.subject] = by_subject.get(q.subject, 0) + 1

        print("generated questions now, and what the weighted targets ask for:\n")
        for s in GENERATED_SUBJECTS:
            if subject and s != subject:
                continue
            want = sum(slot_target(d["id"]) for d in DOMAINS if d["subject"] == s) * len(LEVELS)
            print(f"  {s:<9} {by_subject.get(s, 0):>4} now, target about {want:>4}")

        if not rows:
            print("\nEvery slot is at or under its target. Nothing to prune.")
            return 0

        total = sum(len(r["removable"]) for r in rows)
        kept = sum(r["protected"] for r in rows)
        print(f"\n{len(rows)} slots are over target:\n")
        for r in sorted(rows, key=lambda x: -x["excess"]):
            note = f"   ({r['protected']} of them already served, so kept)" if r["protected"] else ""
            print(f"  {r['subject']:<8} {r['domain']:<14} {r['level']:<11} "
                  f"{r['have']:>3} -> {r['target']:<3} remove {len(r['removable']):>3}{note}")
        print(f"\n  would remove {total}, leaving {kept} slots over target "
              f"because those questions have been served")

        if not apply:
            print("\nDry run. Pass --apply to remove them.")
            return 0

        teacher = db.scalar(select(User).where(User.role == "teacher"))
        if not teacher:
            print("\nNo teacher account exists, and a removal needs an author for its audit.")
            return 1
        for r in rows:
            for q in r["removable"]:
                db.add(Audit(id=str(uuid.uuid4()), user_id=teacher.id, entity_id=q.id,
                             action="pruned_to_target",
                             detail={"domain": q.domain, "difficulty": q.difficulty,
                                     "stem": q.content["stem"][:120],
                                     "slot_had": r["have"], "slot_target": r["target"],
                                     "note": "Generated practice above the weighted target for "
                                             "this sub-topic. Never served to a student."}))
                db.delete(q)
        db.commit()
        print(f"\nRemoved {total} questions.")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--subject", choices=GENERATED_SUBJECTS,
                        help="Limit to one subject.")
    args = parser.parse_args()
    raise SystemExit(run(args.apply, args.subject))
