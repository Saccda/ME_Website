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

# Physics cites two sources and no longer a third. Motion, forces, mechanical
# work, fluids and heat used to follow the topic structure of Mukherji's
# IIT-JEE question bank, because when they were written nothing closer to this
# examination covered those topics. The panel's own bank now does -- it
# examines all five, across its Sections I to III -- so they cite that, and the
# textbook is gone rather than kept as a second opinion on topics the
# examiners have since described themselves.
#
# The 2026 physics panel's own 100-question bank. Its six sections are what the
# examination actually asks, and they reach well past the electrical scope the
# earlier past paper suggested: 75% of it is mechanics, heat, fluids and waves.
# The sub-topics below that cite this source follow its section structure; the
# bank's own 100 items are a separate thing, loaded by tools/import_exam_bank.py
# from a file that is deliberately not in this repository.
PHYSICS_EXAM_BANK_SOURCE = {
    "title": "Mechanical Engineering Entrance Examination, 100-question physics bank",
    "edition": "2026", "publisher": "Royal University of Phnom Penh, Faculty of Engineering",
    "year": 2026, "authors": "ME entrance examination physics panel",
    "basis": (
        "Section structure and question style of the panel's bank. Questions generated under "
        "these sub-topics are written and solved independently; none is copied from the bank, "
        "and none refers to a figure, because a generated question cannot supply one."
    ),
    "mapping_pages": "Sections I–VI, items 1–100",
    "calibration": "Local four-level rubric, calibrated to the bank's own level.",
}

# The examination's Physics section covers mechanics, heat, fluids, waves and
# electricity. The electrical sub-topics follow the past paper; mechanics and
# heat follow the Mukherji structure; the sub-topics added for the panel's bank
# follow its sections. Ordered Foundation -> Challenge like the rest.
# "quantities" rather than "units" because the Mathematics domain above already
# owns that id, and ids are global.
PHYSICS_DOMAINS = [
    # Mechanics and heat follow the topic structure of Parts 1 and 2 of
    # Mukherji, which is an IIT-JEE book: its topics are the examination's,
    # its difficulty is not, so these are written at the level of the past
    # paper above and carry their own source note saying so.
    {"id": "kinematics", "subject": "physics", "name": "Motion in a Straight Line", "sets": "Section I", "source": PHYSICS_EXAM_BANK_SOURCE, "skills": ["speed-distance-time", "acceleration", "equations-of-motion", "free-fall"], "description": "Speed, acceleration and how far a body travels."},
    {"id": "forces", "subject": "physics", "name": "Forces & Newton's Laws", "sets": "Section I", "source": PHYSICS_EXAM_BANK_SOURCE, "skills": ["newton-second-law", "weight", "friction", "resultant-force"], "description": "What a force does to a mass, and what resists it."},
    {"id": "energy", "subject": "physics", "name": "Mechanical Work & Power", "sets": "Section I", "source": PHYSICS_EXAM_BANK_SOURCE, "skills": ["work-done", "kinetic-energy", "potential-energy", "power-output"], "description": "Work done, energy stored and the rate of doing it."},
    {"id": "fluids", "subject": "physics", "name": "Density, Pressure & Fluids", "sets": "Section III", "source": PHYSICS_EXAM_BANK_SOURCE, "skills": ["density", "pressure", "pressure-at-depth", "upthrust"], "description": "Mass per volume, force per area, and what floats."},
    {"id": "thermal", "subject": "physics", "name": "Heat & Thermodynamics", "sets": "Section II", "source": PHYSICS_EXAM_BANK_SOURCE, "skills": ["temperature-scales", "specific-heat", "latent-heat", "gas-laws"], "description": "Temperature, the heat a change needs, and gases."},
    {"id": "current", "subject": "physics", "name": "Charge & Current", "sets": "Q7, Q17–18", "skills": ["charge-flow", "current-from-charge", "charge-rate", "charge-over-minutes"], "description": "Relate charge, current and time."},
    {"id": "ohm", "subject": "physics", "name": "Ohm's Law & Resistance", "sets": "Q1–2", "skills": ["ohms-current", "ohms-voltage", "ohms-resistance", "resistance-from-power"], "description": "Find any one of voltage, current and resistance from the other two."},
    {"id": "networks", "subject": "physics", "name": "Series & Parallel Circuits", "sets": "Q12, Q19–20", "skills": ["series-resistance", "parallel-resistance", "voltage-divider", "network-reduction"], "description": "Reduce a resistor network and divide a voltage."},
    {"id": "power", "subject": "physics", "name": "Electrical Power & Energy", "sets": "Q8–9, Q21–22", "skills": ["power-vi", "power-resistive", "energy-kwh", "power-from-charge"], "description": "Work out power dissipated and energy consumed."},
    # "Electrical" in the name because Mechanical Work & Power now sits beside
    # it. The id is unchanged, so existing questions keep their sub-topic.
    {"id": "work", "subject": "physics", "name": "Electrical Work & Potential", "sets": "Q10, Q14", "skills": ["work-from-charge", "charge-from-work", "potential-difference", "energy-delivered"], "description": "Connect work done, charge moved and potential difference."},
    {"id": "capacitance", "subject": "physics", "name": "Capacitance & Stored Energy", "sets": "Q15–16", "skills": ["capacitance-from-charge", "charge-stored", "energy-stored", "capacitors-combined"], "description": "Charge and energy held by a capacitor."},
    {"id": "quantities", "subject": "physics", "name": "Units, Instruments & Sources", "sets": "Q3–6, Q11, Q13", "skills": ["si-units", "instrument-choice", "source-behaviour", "rms-values"], "description": "Name the unit, pick the instrument, read an AC value."},
    # Added from the 2026 panel's bank, which examines far more than the
    # electrical scope above: 70 of its 100 items had no sub-topic to sit in.
    # Ordered as the bank's own sections are.
    {"id": "momentum", "subject": "physics", "name": "Momentum & Collisions", "sets": "Section I", "source": PHYSICS_EXAM_BANK_SOURCE, "skills": ["momentum", "impulse", "collision-conservation", "recoil-speed"], "description": "Mass in motion, and what survives a collision."},
    {"id": "rotation", "subject": "physics", "name": "Rotation & Circular Motion", "sets": "Section I", "source": PHYSICS_EXAM_BANK_SOURCE, "skills": ["centripetal-acceleration", "angular-speed", "torque", "rotational-energy"], "description": "Turning, and what it takes to change a spin."},
    {"id": "thermo", "subject": "physics", "name": "Thermodynamic Laws & Processes", "sets": "Section II", "source": PHYSICS_EXAM_BANK_SOURCE, "skills": ["process-identification", "first-law", "engine-efficiency", "carnot-efficiency"], "description": "What each process holds fixed, and the limit on an engine."},
    {"id": "flow", "subject": "physics", "name": "Fluid Flow & Hydraulics", "sets": "Section III", "source": PHYSICS_EXAM_BANK_SOURCE, "skills": ["continuity", "hydraulic-force", "efflux-speed", "reynolds-number"], "description": "Moving fluid: continuity, pressure multiplied, and flow regime."},
    {"id": "waves", "subject": "physics", "name": "Waves & Oscillations", "sets": "Section IV", "source": PHYSICS_EXAM_BANK_SOURCE, "skills": ["wave-equation", "pendulum-period", "harmonic-motion", "string-harmonics"], "description": "Period, wavelength and speed, and what resonates."},
    {"id": "fields", "subject": "physics", "name": "Electric & Magnetic Fields", "sets": "Sections V–VI", "source": PHYSICS_EXAM_BANK_SOURCE, "skills": ["coulomb-force", "field-force", "magnetic-force", "induced-emf"], "description": "Force on a charge or a current, and emf from changing flux."},
    {"id": "ac", "subject": "physics", "name": "AC Circuits & Reactance", "sets": "Section V", "source": PHYSICS_EXAM_BANK_SOURCE, "skills": ["rms-conversion", "inductive-reactance", "capacitive-reactance", "series-impedance"], "description": "What a coil and a capacitor do to alternating current."},
    # Added from the real paper rather than from the bank. Its first page is
    # eight unit questions -- which unit measures speed, which is the
    # equivalent unit of force, what 1 kPa or 1 kWh is equal to -- where the
    # panel's 100-question bank has two unit questions in total. The bank
    # under-represents this, so the paper is the authority here.
    # No "source" key, so it falls back to PHYSICS_SOURCE, the past paper --
    # which is the right citation and is declared further down the file.
    {"id": "conversion", "subject": "physics", "name": "Units & Conversions", "sets": "Paper page 1", "skills": ["unit-of-quantity", "derived-unit", "unit-equivalence", "prefix-conversion"], "description": "Which unit measures what, and what equals what."},
]

DOMAINS = LOGIC_DOMAINS + MATH_DOMAINS + PHYSICS_DOMAINS

# How many of the real paper's questions each sub-topic carries.
#
# Logic and Mathematics come from the panel's own control sheets, which set out
# 25 questions per subject against named topics. Physics has no control sheet,
# so it follows the section sizes of the panel's 100-question bank, divided
# between the sub-topics that cover each section.
#
# The seeder reads these to decide how much practice to generate per sub-topic,
# so practice is weighted the way the examination is rather than spread evenly
# over topics that carry very different numbers of marks. A weight of 0 means
# the sheet does not examine that sub-topic at all; it still gets a floor, so
# the groundwork stays practisable, but it is not grown.
EXAM_WEIGHTS = {
    # --- Logic: control sheet, 25 questions. Our sub-topics follow the
    # sheet's own set ranges exactly, so each weight is its ranges added up.
    "patterns": 4,       # Sets 1-4, Number Series
    "symbols": 3,        # Sets 5-6, Letter and Symbol Series
    "relationships": 11,  # Sets 7-8 Verbal Classification 3, 9-11 Essential Part 4, 12-17 Analogies 4
    "codes": 1,          # Sets 18-19, Artificial Language
    "verbal": 3,         # Set 20 Matching Definitions, 21 Making Judgments, 22 Verbal Reasoning
    "deduction": 2,      # Sets 23-27 Logic Problems, 28-31 Logic Games
    "arguments": 1,      # Sets 32-37, Analyzing Arguments

    # --- Mathematics: control sheet, 25 questions. Three sub-topics score 0
    # because the sheet does not examine them, and 10 of its 25 marks have no
    # sub-topic to sit in at all: Determinants (3), Dot & Cross Product (3),
    # Quadratic (2) and Limit (2). See docs/ROADMAP.md.
    "graphs": 3,         # Algebra and Function / Straight-line graph
    "algebra": 2,        # Algebra and Function / Quadratic -- not yet a template
    "calculus": 14,      # Limit 2, Differentiation 4, Indefinite Integral 4, Definite Integral 4
    "vectors": 3,        # Vector Algebra / Dot & Cross Product -- not yet a template
    "number": 0,         # Number & Proportion: groundwork, not examined
    "triangles": 0,      # Angles & Triangles: groundwork, not examined
    "units": 0,          # Units & Engineering Notation: groundwork, not examined

    # --- Physics: the real paper, question by question. Its 30 questions are
    # 50 of the 100 marks.
    #
    # These replace weights inferred from the panel's 100-question bank, which
    # turned out not to describe the paper at all. The bank is a quarter waves
    # and electromagnetism; the paper has none of either, nor thermodynamics,
    # momentum or rotation. It is units and circuits, with a little kinematics,
    # energy and fluid pressure -- so the four sub-topics the bank weighted
    # most heavily are the four the paper never asks.
    "conversion": 9,   # Q1-Q8 units and equivalences, Q16 powers of ten
    "networks": 7,     # Q20, Q23-Q26, Q29, Q30 -- equivalent R, dividers, mesh and node
    "kinematics": 3,   # Q9 deceleration, Q10 fall from a moving truck, Q11 a(t)
    "energy": 2,       # Q12 energy wasted per second, Q13 kettle efficiency
    "fluids": 2,       # Q14 hydrostatic head, Q15 closed tube
    "ohm": 2,          # Q17 V from P and I, Q19 R from V and I
    "power": 2,        # Q22 I^2Rt, Q27 AC active power
    "quantities": 2,   # Q21 which is not electrical, Q28 unit of charge
    "current": 1,      # Q18 I as dQ/dt
    # Not on the paper. They keep the floor, so a student who wants them finds
    # something and the panel's bank still has a home, but nothing grows here.
    "forces": 0, "thermal": 0, "thermo": 0, "flow": 0, "waves": 0,
    "momentum": 0, "rotation": 0, "fields": 0, "ac": 0,
    "work": 0, "capacitance": 0,
    # Provisional, and the one weight here not derived from a whole document.
    # Page 1 of the real paper is eight unit questions; if the physics section
    # is 30 questions and eight of them are units, this should be nearer 36
    # than 8, which would make it the heaviest physics sub-topic by some way.
    # Eight is what can be justified from what has actually been seen. Raise it
    # once the paper's full unit count is known.
    "conversion": 8,
}
assert set(EXAM_WEIGHTS) == {d["id"] for d in DOMAINS}, "every sub-topic needs a weight"

LEVELS = ["Foundation", "Practice", "Exam Level", "Challenge"]
LEVEL_GUIDE = {
    "Foundation": "One explicit rule or relationship; short stem.",
    "Practice": "Two connected steps or a repeating rule.",
    "Exam Level": "Combine constraints; distinguish plausible alternatives.",
    "Challenge": "Multiple constraints or a hidden assumption; extended reasoning.",
}

LOGIC_SOURCE = {"title": "501 Challenging Logic and Reasoning Problems", "edition": "2nd", "publisher": "LearningExpress, LLC", "year": 2005, "isbn": "1-57685-534-1", "basis": "Structure and reasoning families only. Original question; no source question copied.", "mapping_pages": "Introduction, printed viii; PDF page 8", "calibration": "Local four-level rubric inspired by the book's progression; not an official exam calibration."}
MATH_SOURCE = {"title": "Mechanical Engineering Principles", "edition": "3rd", "publisher": "Routledge", "year": 2019, "authors": "John Bird, Carl Ross", "basis": "Topic structure of Part One, Revision of Mathematics, only. Every question is generated and solved independently; no source question copied.", "mapping_pages": "Part One, Chapters 1–2; PDF pages 12–55", "calibration": "Local four-level rubric; not an official RUPP entrance calibration."}
PHYSICS_SOURCE = {"title": "Past entrance examination paper, Physics section", "edition": "—", "publisher": "Royal University of Phnom Penh, Faculty of Engineering", "year": 2026, "basis": "Topic scope and question style of the paper's 22 items only. Every question is generated and solved independently; no paper question copied, and no question refers to a figure, because a generated question cannot supply a circuit diagram.", "mapping_pages": "Section I, items 1–22", "calibration": "Local four-level rubric; not an official RUPP entrance calibration."}

SUBJECTS = [
    {"id": "logic", "short": "Logic", "name": "Logic & Reasoning", "description": "Reasoning that needs no formula.", "domains": [d["id"] for d in LOGIC_DOMAINS], "source": LOGIC_SOURCE},
    {"id": "math", "short": "Mathematics", "name": "Mathematics", "description": "The mathematics an engineering course expects on day one.", "domains": [d["id"] for d in MATH_DOMAINS], "source": MATH_SOURCE},
    # Was "the electrical principles the examination asks for", which the 2026
    # panel's bank showed to be too narrow: only a quarter of it is electrical.
    {"id": "physics", "short": "Physics", "name": "Physics", "description": "Mechanics, heat, fluids, waves and electricity, as the examination asks them.", "domains": [d["id"] for d in PHYSICS_DOMAINS], "source": PHYSICS_SOURCE},
]
SOURCES = {"logic": LOGIC_SOURCE, "math": MATH_SOURCE, "physics": PHYSICS_SOURCE}

# Subjects whose generator templates exist; the seeder only fills these.
GENERATED_SUBJECTS = ("logic", "math", "physics")

SUBJECT_OF = {d["id"]: d["subject"] for d in DOMAINS}
DOMAIN_BY_ID = {d["id"]: d for d in DOMAINS}

# Kept so existing imports of a single logic source keep working.
SOURCE = LOGIC_SOURCE
