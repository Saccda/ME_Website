"""Create the mock exam that matches the real entrance examination.

The paper is 80 multiple-choice questions in 1 hour 30 minutes: 25
Mathematics, 25 Logic, 30 Physics, four options each. That is three rows, one
per section, and the sections are sat in order.

    python tools/create_exam_blueprint.py                  # report only
    python tools/create_exam_blueprint.py --apply
    python tools/create_exam_blueprint.py --apply --draft  # not yet visible
    python tools/create_exam_blueprint.py --apply --mixed-physics

Running it again updates the paper it made before rather than adding a second
one, so it is safe to re-run after approving more questions.

The physics section draws on the examination panel's own bank, which
tools/import_exam_bank.py loads; --mixed-physics widens it to the generated
questions too.

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


# Mathematics, from the panel's control sheet. Straight-line graph 3, Quadratic
# 2, Limit 2, Differentiation 4, Indefinite Integral 4, Definite Integral 4,
# Determinants 3, Dot & Cross Product 3.
#
# Four of those topics have no template yet, so this cannot be exact. Calculus
# carries the sheet's 14 marks for limits, differentiation and integration.
# Quadratic and Dot & Cross are drawn from the nearest sub-topics we do have,
# which examine the right area at the wrong skill. Determinants has nothing at
# all, so its 3 marks are taken from Mathematics at large rather than shortening
# the paper -- see ROADMAP item 1.
MATH_ROWS = [
    {"subject": "math", "domain": "graphs", "count": 3, "options": 4},
    {"subject": "math", "domain": "algebra", "count": 2, "options": 4},
    {"subject": "math", "domain": "calculus", "count": 14, "options": 4},
    {"subject": "math", "domain": "vectors", "count": 3, "options": 4},
    # Determinants, standing in. A second algebra row rather than a loose
    # "3 from Mathematics", which drew from Number & Proportion, Angles &
    # Triangles and Units -- three sub-topics the sheet does not examine, so
    # every paper carried a question no candidate will be asked.
    {"subject": "math", "domain": "algebra", "count": 3, "options": 4},
]

# Logic, from the control sheet, and this one is exact: our sub-topics follow
# the sheet's own set ranges, so each row is a range and its mark count.
LOGIC_ROWS = [
    {"subject": "logic", "domain": "patterns", "count": 4, "options": 4},
    {"subject": "logic", "domain": "symbols", "count": 3, "options": 4},
    {"subject": "logic", "domain": "relationships", "count": 11, "options": 4},
    {"subject": "logic", "domain": "codes", "count": 1, "options": 4},
    {"subject": "logic", "domain": "verbal", "count": 3, "options": 4},
    {"subject": "logic", "domain": "deduction", "count": 2, "options": 4},
    {"subject": "logic", "domain": "arguments", "count": 1, "options": 4},
]


# How many of the paper's 30 physics questions are units.
#
# Page 1 of the real paper is eight unit questions and the panel's bank has two
# in the whole document, so a physics section drawn entirely from the bank
# cannot carry them. These are drawn from the generated Units & Conversions
# sub-topic instead -- the only place in this paper where a generated question
# stands in for the panel's own, and only because the panel's material does not
# cover what its own paper asks.
#
# Eight is what page 1 shows. If the paper's real unit count differs, this is
# the number to change.
PHYSICS_UNIT_QUESTIONS = 8


def rows_for(physics_origin):
    """The three sections, sat in the order written here.

    Named sub-topic by sub-topic rather than "25 Mathematics, 25 Logic". A row
    naming only a subject draws at random from everything approved in it, which
    tracks the sheet only as closely as the bank happens to be shaped: measured,
    that gave Logic 1.8 Classification questions against the sheet's 11, while
    Number Series got 7.8 against its 4, and it put questions from three
    Mathematics sub-topics the sheet does not examine at all into every paper.
    A student sitting this should meet the topics they will actually be
    examined on, in the proportions they will meet them.

    Physics stays a single row because it draws on the panel's own bank, whose
    100 questions already carry the examination's section mix -- 25 Mechanics,
    20 Thermodynamics, 15 Fluids, 15 Waves, 13 Electricity, 12 Electromagnetism
    -- so a random 30 from it is already in proportion.
    """
    units = {"subject": "physics", "domain": "conversion",
             "count": PHYSICS_UNIT_QUESTIONS, "options": 4}
    rest = {"subject": "physics", "count": 30 - PHYSICS_UNIT_QUESTIONS, "options": 4}
    if physics_origin:
        rest["origin"] = physics_origin
    return MATH_ROWS + LOGIC_ROWS + [units, rest]


def origin_of(q):
    kind = q.source.get("kind")
    if kind in ("textbook-excerpt", "adapted-textbook"):
        return "textbook"
    return "exam-bank" if kind == "exam-bank" else "original"


def available(db, row):
    questions = db.scalars(
        select(Question).where(Question.status == "approved",
                               Question.subject == row["subject"])
    ).all()
    return sum(1 for q in questions
               if len(q.content["options"]) == row["options"]
               and (not row.get("domain") or q.domain == row["domain"])
               and (not row.get("origin") or origin_of(q) == row["origin"]))


def label(row):
    return f"{row['subject']}/{row['domain']}" if row.get("domain") else row["subject"]


def run(apply, draft, physics_origin):
    ROWS = rows_for(physics_origin)
    with SessionLocal() as db:
        print(f"{NAME}  ·  {MINUTES} minutes  ·  {sum(r['count'] for r in ROWS)} questions\n")
        short = []
        for row in ROWS:
            have = available(db, row)
            flag = "" if have >= row["count"] else "   <-- NOT ENOUGH"
            drawn = f" from the {row['origin']}" if row.get("origin") else ""
            print(f"  {label(row):>22}: {row['count']:>3} needed, {have:>4} approved with "
                  f"{row['options']} options{drawn}{flag}")
            if have < row["count"]:
                short.append(f"{label(row)} (needs {row['count']}, has {have})")

        existing = db.scalar(select(Blueprint).where(Blueprint.name == NAME))
        print(f"\nthis paper already exists: {'yes, it will be updated' if existing else 'no'}")
        if existing:
            # What the counts above describe is the paper this run *would*
            # write, not the one students are being given. Without printing the
            # stored rows a dry run looks identical whether or not they already
            # match, which is no use to someone checking whether an earlier run
            # landed.
            print(f"  stored: published={existing.published}, {existing.minutes} minutes")
            for row in existing.rows:
                drawn = f", from the {row['origin']}" if row.get("origin") else ""
                print(f"    {row.get('subject') or row.get('domain')}: "
                      f"{row['count']} x {row['options']} options{drawn}")
            if existing.rows == ROWS and existing.minutes == MINUTES:
                print("  the stored paper already matches; --apply would change nothing")
            else:
                print("  this differs from what --apply would write, shown above")

        if short and not draft:
            print("\nCannot publish yet -- short in: " + ", ".join(short))
            print("Approve more questions first, or pass --draft to save it unpublished.")
            if any(r.get("origin") == "exam-bank" for r in ROWS):
                print("If the panel's bank is not loaded yet: "
                      "python tools/import_exam_bank.py --apply")
                print("To build the paper from generated physics instead: --mixed-physics")
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
    parser.add_argument("--mixed-physics", action="store_true",
                        help="Draw physics from the whole approved bank rather than only "
                             "the examination panel's own questions.")
    args = parser.parse_args()
    raise SystemExit(run(args.apply, args.draft,
                         None if args.mixed_physics else "exam-bank"))
