"""Subjects, their topic domains, and the shared level rubric.

A domain belongs to exactly one subject. DOMAINS stays a flat list of every
domain so existing lookups by domain id keep working unchanged; SUBJECTS groups
them for the catalogue API and for filtering.

Mathematics follows Part One, Revision of Mathematics, of Bird & Ross, which is
the level a student entering the programme is expected to revise. Structure and
topic families only -- no question is copied from any book.
"""

LOGIC_DOMAINS = [
    {"id": "patterns", "subject": "logic", "name": "Number & Pattern Reasoning", "sets": "1–4", "skills": ["constant-step", "growing-differences", "alternating-rules", "two-step-recurrence"], "description": "Find the rule. Test it against every term."},
    {"id": "symbols", "subject": "logic", "name": "Letter & Symbol Reasoning", "sets": "5–6", "skills": ["alphabet-steps", "symbol-cycles", "paired-letter-number", "alternating-letter-steps"], "description": "Track positions, changes, and repeating cycles."},
    {"id": "relationships", "subject": "logic", "name": "Classification & Relationships", "sets": "7–17", "skills": ["classification", "function-analogy", "essential-part", "relationship-chain"], "description": "Identify what belongs and how ideas connect."},
    {"id": "codes", "subject": "logic", "name": "Coded Language Reasoning", "sets": "18–19", "skills": ["word-components", "three-component-code", "reverse-decoding", "code-elimination"], "description": "Use shared clues to decode unfamiliar words."},
    {"id": "verbal", "subject": "logic", "name": "Applied Verbal Reasoning", "sets": "20–22", "skills": ["matching-definitions", "necessary-condition", "must-be-true", "multi-condition-judgment"], "description": "Apply definitions and make evidence-based judgments."},
    {"id": "deduction", "subject": "logic", "name": "Deductive Logic & Logic Games", "sets": "23–31", "skills": ["ordering", "constrained-ordering", "conditional-ordering", "multi-constraint-puzzle"], "description": "Combine constraints to find what must be true."},
    {"id": "arguments", "subject": "logic", "name": "Critical & Argument Reasoning", "sets": "32–37", "skills": ["conclusion", "assumption", "weakening-evidence", "causal-confounding"], "description": "Separate evidence, assumptions, and conclusions."},
]

# Each skill list is ordered Foundation → Practice → Exam Level → Challenge, so
# a difficulty selects the skill at that index.
MATH_DOMAINS = [
    {"id": "number", "subject": "math", "name": "Number & Proportion", "sets": "1.6–1.7", "skills": ["fractions", "percentages", "ratio-proportion", "percentage-change"], "description": "Work with fractions, ratios and percentage change."},
    {"id": "algebra", "subject": "math", "name": "Algebra & Equations", "sets": "1.5, 1.8–1.9", "skills": ["brackets", "laws-of-indices", "linear-equation", "simultaneous-equations"], "description": "Expand, simplify and solve for the unknown."},
    {"id": "triangles", "subject": "math", "name": "Angles & Triangles", "sets": "1.2–1.4", "skills": ["radians-degrees", "right-triangle-ratios", "pythagoras", "triangle-solution"], "description": "Convert angles and solve triangles."},
    {"id": "units", "subject": "math", "name": "Units & Engineering Notation", "sets": "2.1–2.2", "skills": ["si-prefixes", "engineering-notation", "unit-conversion", "compound-units"], "description": "Carry units and powers of ten without losing the quantity."},
    {"id": "graphs", "subject": "math", "name": "Graphs & Gradients", "sets": "2.3–2.5", "skills": ["straight-line-value", "gradient", "intercept", "practical-graph"], "description": "Read a straight line and state its equation."},
    {"id": "calculus", "subject": "math", "name": "Introductory Calculus", "sets": "2.6–2.9", "skills": ["differentiation", "rate-of-change", "integration", "definite-integral"], "description": "Differentiate and integrate simple polynomials."},
    {"id": "vectors", "subject": "math", "name": "Vectors", "sets": "2.10", "skills": ["vector-components", "resultant-magnitude", "vector-direction", "vector-addition"], "description": "Resolve and combine quantities that have direction."},
]

DOMAINS = LOGIC_DOMAINS + MATH_DOMAINS

LEVELS = ["Foundation", "Practice", "Exam Level", "Challenge"]
LEVEL_GUIDE = {
    "Foundation": "One explicit rule or relationship; short stem.",
    "Practice": "Two connected steps or a repeating rule.",
    "Exam Level": "Combine constraints; distinguish plausible alternatives.",
    "Challenge": "Multiple constraints or a hidden assumption; extended reasoning.",
}

LOGIC_SOURCE = {"title": "501 Challenging Logic and Reasoning Problems", "edition": "2nd", "publisher": "LearningExpress, LLC", "year": 2005, "isbn": "1-57685-534-1", "basis": "Structure and reasoning families only. Original question; no source question copied.", "mapping_pages": "Introduction, printed viii; PDF page 8", "calibration": "Local four-level rubric inspired by the book's progression; not an official exam calibration."}
MATH_SOURCE = {"title": "Mechanical Engineering Principles", "edition": "3rd", "publisher": "Routledge", "year": 2019, "authors": "John Bird, Carl Ross", "basis": "Topic structure of Part One, Revision of Mathematics, only. Every question is generated and solved independently; no source question copied.", "mapping_pages": "Part One, Chapters 1–2; PDF pages 12–55", "calibration": "Local four-level rubric; not an official RUPP entrance calibration."}

SUBJECTS = [
    {"id": "logic", "short": "Logic", "name": "Logic & Reasoning", "description": "Reasoning that needs no formula.", "domains": [d["id"] for d in LOGIC_DOMAINS], "source": LOGIC_SOURCE},
    {"id": "math", "short": "Mathematics", "name": "Mathematics", "description": "The mathematics an engineering course expects on day one.", "domains": [d["id"] for d in MATH_DOMAINS], "source": MATH_SOURCE},
]
SOURCES = {"logic": LOGIC_SOURCE, "math": MATH_SOURCE}

# Subjects whose generator templates exist; the seeder only fills these.
GENERATED_SUBJECTS = ("logic", "math")

SUBJECT_OF = {d["id"]: d["subject"] for d in DOMAINS}
DOMAIN_BY_ID = {d["id"]: d for d in DOMAINS}

# Kept so existing imports of a single logic source keep working.
SOURCE = LOGIC_SOURCE
