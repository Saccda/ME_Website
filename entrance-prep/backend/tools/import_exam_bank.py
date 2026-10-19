"""Load the examination panel's own physics bank into the question table.

The bank is the panel's work, not ours, and it reveals what the real paper
asks. This repository is public, so the questions are NOT in it: they live in
entrance-prep/private/, which .gitignore already keeps out of version control
for licensed reference material, and the file is carried to the lab by hand.
This tool is the part that is safe to publish, review and re-run.

    python tools/import_exam_bank.py                      # report only
    python tools/import_exam_bank.py --apply
    python tools/import_exam_bank.py --apply --draft      # import unapproved
    python tools/import_exam_bank.py --file /path/to.json

Re-running updates the questions it imported before rather than adding a second
copy, matching on the `ref` it records in each question's source, so it is safe
after the panel revises an item.

Every question is put through the same validator the generators are held to
before anything is written. The 29 computable answers carry a `compute` spec
and are recomputed here; the rest are structural checks only, because a
question asking which formula is Ohm's law has no arithmetic to repeat. The
whole file is refused if any single question fails, rather than importing the
good ones and leaving a partial bank nobody can account for.

Imported questions are approved on arrival, unlike generated seeds, which stay
drafts for local review. The reason is that the author here is the examination
panel itself and the keys were checked item by item before the file was built;
making a teacher re-approve 100 questions they commissioned would be theatre.
Pass --draft if you would rather review them in Teacher studio first.
"""
import argparse
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sqlalchemy import select  # noqa: E402
from app.catalog import DOMAIN_BY_ID, LEVELS, PHYSICS_EXAM_BANK_SOURCE, SUBJECT_OF  # noqa: E402
from app.models import SessionLocal, Question, User, Audit  # noqa: E402
from app.validation import validate  # noqa: E402

DEFAULT_FILE = Path(__file__).resolve().parents[2] / "private" / "exam_bank.json"
# Read by the origin filter, so a mock exam row can ask for the real paper's
# own questions while ordinary practice still draws on everything.
KIND = "exam-bank"


def content_of(entry):
    """The stored content dict, in the shape the generators produce."""
    return {
        "stem": entry["stem"],
        "options": [{"id": "ABCDE"[i], "text": o["text"],
                     "rationale": o["rationale"], "error": o["error"]}
                    for i, o in enumerate(entry["options"])],
        "correct": entry["correct"],
        "explanation": entry["explanation"],
        "math": entry.get("math"),
        "presentation": "text",
        "asset": None,
        "asset_alt": "",
        "diagram": None,
        "validator": entry.get("validator"),
    }


def check(entries):
    """Every reason this file must not be imported, collected in one pass."""
    problems = []
    refs = [e.get("ref") for e in entries]
    if len(set(refs)) != len(refs):
        problems.append("The file contains two questions with the same ref.")
    for entry in entries:
        ref = entry.get("ref", "?")
        domain = DOMAIN_BY_ID.get(entry.get("domain", ""))
        if not domain:
            problems.append(f"{ref}: unknown sub-topic {entry.get('domain')!r}")
            continue
        if SUBJECT_OF[entry["domain"]] != entry.get("subject"):
            problems.append(f"{ref}: {entry['domain']} is not part of {entry.get('subject')!r}")
        if entry.get("skill") not in domain["skills"]:
            problems.append(f"{ref}: {entry.get('skill')!r} is not a skill of {entry['domain']}")
        if entry.get("difficulty") not in LEVELS:
            problems.append(f"{ref}: unknown level {entry.get('difficulty')!r}")
        report = validate(content_of(entry))
        if not report["passed"]:
            problems.append(f"{ref}: " + "; ".join(report["errors"]))
    return problems


def run(apply, draft, path):
    if not path.exists():
        print(f"No question file at {path}")
        print("It is deliberately not in this repository. Copy it to that path first.")
        return 1
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != 1:
        print(f"Unsupported file schema {payload.get('schema')!r}; this tool reads schema 1.")
        return 1
    entries = payload["questions"]

    problems = check(entries)
    print(f"{path.name}: {len(entries)} questions\n")
    if problems:
        print(f"Refusing to import. {len(problems)} problem(s):")
        for p in problems[:20]:
            print(f"  {p}")
        if len(problems) > 20:
            print(f"  ... and {len(problems) - 20} more")
        return 1

    proved = sum(1 for e in entries if e.get("validator"))
    letters = {}
    for e in entries:
        letters[e["correct"]] = letters.get(e["correct"], 0) + 1
    print(f"  validator passed            : {len(entries)}/{len(entries)}")
    print(f"  recomputed from their values: {proved}")
    print(f"  answer letters              : " +
          ", ".join(f"{k} {v}" for k, v in sorted(letters.items())))

    with SessionLocal() as db:
        known = {q.source.get("ref"): q
                 for q in db.scalars(select(Question).where(Question.subject == "physics"))
                 if q.source.get("kind") == KIND}
        fresh = [e for e in entries if e["ref"] not in known]
        print(f"  already imported            : {len(entries) - len(fresh)}")
        print(f"  new                         : {len(fresh)}")

        if not apply:
            print("\nDry run. Pass --apply to write them.")
            return 0

        teacher = db.scalar(select(User).where(User.role == "teacher"))
        if not teacher:
            print("\nNo teacher account exists, and an import needs an author for its audit.")
            return 1

        status = "draft" if draft else "approved"
        for entry in entries:
            content = content_of(entry)
            report = validate(content)
            source = {**PHYSICS_EXAM_BANK_SOURCE, "kind": KIND, "ref": entry["ref"],
                      "sets": DOMAIN_BY_ID[entry["domain"]]["sets"],
                      "basis": ("Question, options and answer key are the examination panel's "
                                "own. Option order was redistributed so that each letter is "
                                "correct equally often, and formula options were set as LaTeX so "
                                "the browser typesets them -- the paper has no typesetting, so a "
                                "radical reached a reader as a bare glyph with no bar over what "
                                "it covers. The mathematics and the key are unchanged. "
                                "Distractor rationales are newly authored.")}
            previous = known.get(entry["ref"])
            if previous:
                previous.domain = entry["domain"]
                previous.skill = entry["skill"]
                previous.difficulty = entry["difficulty"]
                previous.content = content
                previous.source = source
                previous.validation = report
                previous.version += 1
                qid, action = previous.id, "exam_bank_updated"
            else:
                qid, action = str(uuid.uuid4()), "exam_bank_imported"
                db.add(Question(id=qid, subject="physics", domain=entry["domain"],
                                skill=entry["skill"], difficulty=entry["difficulty"],
                                status=status, content=content, source=source,
                                validation=report, version=1))
            db.add(Audit(id=str(uuid.uuid4()), user_id=teacher.id, entity_id=qid, action=action,
                         detail={"ref": entry["ref"], "domain": entry["domain"],
                                 "status": status, "recomputed": bool(entry.get("validator")),
                                 "note": payload.get("note", "")}))
        db.commit()

    print(f"\nImported as {status}: {len(fresh)} new, {len(entries) - len(fresh)} updated.")
    if draft:
        print("Approve them in Teacher studio before students can be given them.")
    else:
        print("Build the mock exam next: python tools/create_exam_blueprint.py --apply")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--draft", action="store_true",
                        help="Import unapproved, for review in Teacher studio first.")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE)
    args = parser.parse_args()
    raise SystemExit(run(args.apply, args.draft, args.file))
