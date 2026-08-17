"""Fill in the Composite Particle Board project page as a worked example.

The project began as a sugarcane study and has widened: bagasse, coconut shell
and small waste plastics are now all being tried, so the page is written as a
comparison between feedstocks rather than an argument for one of them.

Written as a draft an author corrects, not as a record of results. Everything
that would need verifying before publication is marked, and the page states no
measured outcome, because none has been supplied. What it does show is the
shape a research project page should take: what the work is for, how it is
being done, who is doing it, and what has actually happened so far.

Names are left as roles. A student's name on a public university page needs
their agreement first, and that is not something a seeding command can give.

The command also renames the record if it is still under its old sugarcane
slug, so an existing project is carried across rather than duplicated.

    python manage.py seed_composite_board_project
"""

from django.core.management.base import BaseCommand
from wagtail.rich_text import RichText

from program.models import ResearchProject

SLUG = "composite-particle-board"
OLD_SLUG = "sugarcane-particle-board"
TITLE = "Composite Particle Board"

SUMMARY = (
    "Cambodia produces more residue than it currently uses: bagasse from the "
    "sugar mills, shell from coconut processing, and plastic fragments too "
    "small and too mixed to be recycled conventionally. This project asks "
    "which of them can be bound into a particle board strong enough for "
    "practical use, and what each one costs in strength, moisture resistance "
    "and ease of manufacture."
)

BODY = [
    (
        "paragraph",
        RichText(
            "<p>The project started with a single material. Bagasse is what "
            "remains once sugarcane has been crushed for juice: it is produced "
            "in quantity, it is cheap, and much of it is burned or left to "
            "decay. A material with that profile is worth examining as an "
            "engineering input rather than a waste stream.</p>"
            "<p>Working with it raised the obvious next question. Bagasse is "
            "not the only residue Cambodia has in volume, and the same press, "
            "the same binder and the same tests can be pointed at others. The "
            "work now compares three feedstocks rather than arguing for "
            "one.</p>"
            "<p>The question is a narrow one, and deliberately so: can these "
            "residues be bound into a board whose strength, moisture behaviour "
            "and manufacturability are good enough for real use, and which of "
            "them does it best? A negative answer, clearly demonstrated, would "
            "be a useful result too.</p>"
        ),
    ),
    (
        "table",
        {
            "heading": "Feedstocks under test",
            "table": {
                "first_row_is_table_header": True,
                "first_col_is_header": False,
                "data": [
                    {
                        "data": [
                            "Material",
                            "Where it comes from",
                            "Why it is being tried",
                            "What is still uncertain",
                        ]
                    },
                    {
                        "data": [
                            "Sugarcane bagasse",
                            "Sugar milling residue",
                            "Long fibres that may carry load in bending",
                            "It absorbs readily, so moisture behaviour is the "
                            "open question",
                        ]
                    },
                    {
                        "data": [
                            "Coconut shell",
                            "Coconut processing waste",
                            "Hard and dense once milled; may add stiffness and "
                            "dimensional stability",
                            "A rigid filler rather than a fibre, so it may "
                            "make the board brittle and heavy",
                        ]
                    },
                    {
                        "data": [
                            "Small waste plastics",
                            "Post-consumer fragments below the size sorting "
                            "lines handle",
                            "Thermoplastic, so it can melt and bind the other "
                            "particles instead of a separate resin",
                            "Mixed polymer types soften at different "
                            "temperatures, so consistency is the open question",
                        ]
                    },
                ],
            },
            "caption": (
                "Each material is tried on its own before any blend, so a "
                "later result can be attributed to one of them."
            ),
        },
    ),
    (
        "steps",
        {
            "heading": "Approach",
            "steps": [
                {
                    "title": "Review reinforcement options",
                    "description": (
                        "Survey the binders and reinforcement strategies "
                        "already reported for agricultural-residue and "
                        "plastic-bound boards, and narrow them to those "
                        "workable with equipment and materials available "
                        "locally."
                    ),
                },
                {
                    "title": "Prepare and characterise each residue",
                    "description": (
                        "Establish a repeatable preparation route for every "
                        "feedstock -- drying, milling, particle size, moisture "
                        "content -- so that later specimens differ by design "
                        "rather than by accident."
                    ),
                },
                {
                    "title": "Hold the process constant",
                    "description": (
                        "Fix press temperature, pressure, time and panel "
                        "geometry across the trials, so that a board differs "
                        "from another by its material and not by how it "
                        "happened to be made."
                    ),
                },
                {
                    "title": "Produce trial panels",
                    "description": (
                        "Press single-material specimens first, then blends, "
                        "across a range of binder ratios and compaction "
                        "conditions."
                    ),
                },
                {
                    "title": "Test and compare",
                    "description": (
                        "Measure bending strength, internal bond, density and "
                        "moisture behaviour against the requirements a usable "
                        "board would have to meet, and compare the feedstocks "
                        "on the same terms."
                    ),
                },
                {
                    "title": "Weigh more than strength",
                    "description": (
                        "Judge each option on cost, availability and "
                        "preparation effort as well as performance. A board "
                        "that tests well but cannot be made from what is "
                        "actually to hand is not a result worth reporting as "
                        "one."
                    ),
                },
            ],
        },
    ),
    (
        "team",
        {
            "heading": "Project team",
            "members": [
                {
                    "name": "Student researcher",
                    "role": "Lead investigator",
                    "detail": "Preparation, specimen production and testing",
                },
                {
                    "name": "Student researcher",
                    "role": "Investigator",
                    "detail": "Literature review and material characterisation",
                },
                {
                    "name": "ME teaching staff",
                    "role": "Supervisor",
                    "detail": "Method, laboratory safety and reporting",
                },
            ],
        },
    ),
    (
        "timeline",
        {
            "heading": "Project activities",
            "entries": [
                {
                    "period": "Early 2026",
                    "title": "Literature review of reinforcement options",
                    "detail": (
                        "Reviewed reported approaches to reinforcing "
                        "agricultural-residue boards and shortlisted those "
                        "achievable with available equipment."
                    ),
                    "status": "done",
                },
                {
                    "period": "4 August 2026",
                    "title": "Progress presented at the Tuesday Weekly Seminar",
                    "detail": (
                        "The team presented the reinforcement review and an "
                        "update on polymer binder reinforced with sugarcane "
                        "bagasse, and took questions from staff and students."
                    ),
                    "status": "done",
                },
                {
                    "period": "August 2026",
                    "title": "Study widened beyond sugarcane",
                    "detail": (
                        "Coconut shell and small waste plastics were added as "
                        "feedstocks, turning a single-material study into a "
                        "comparison across three residues."
                    ),
                    "status": "done",
                },
                {
                    "period": "Current",
                    "title": "Trial panel production across feedstocks",
                    "detail": (
                        "Producing specimens from each residue in turn, across "
                        "a range of binder ratios and compaction conditions, "
                        "with the press settings held constant."
                    ),
                    "status": "current",
                },
                {
                    "period": "Next",
                    "title": "Mechanical and moisture testing",
                    "detail": (
                        "Testing specimens and comparing the feedstocks "
                        "against the requirements for a usable board."
                    ),
                    "status": "planned",
                },
            ],
        },
    ),
    # Straight after the activities, because the timeline says what happened
    # and the gallery shows it. It is also where credit sits: the pictures are
    # of the team's own work.
    (
        "media_gallery",
        {
            "heading": "Activities in the laboratory",
            "caption": (
                "Preparation, specimen production and testing, carried out by "
                "the project team."
            ),
            "items": [],
        },
    ),
    (
        "callout",
        {
            "label": "Status",
            "text": (
                "This project is running. No performance figures are published "
                "yet, and none should be quoted until testing is complete and "
                "the results have been reviewed. Nothing here says that one "
                "feedstock has outperformed another."
            ),
        },
    ),
    (
        "paragraph",
        RichText(
            "<p>Work of this kind is how students learn what engineering "
            "research actually involves: choosing a question narrow enough to "
            "answer, building a method that produces comparable specimens, and "
            "reporting what the results show rather than what was hoped for. "
            "The materials are local, and so is the problem they address.</p>"
        ),
    ),
]


class Command(BaseCommand):
    help = (
        "Fill in the Composite Particle Board project as a worked example of "
        "the research page layout, renaming it from the older sugarcane slug "
        "if necessary. Overwrites that project's body."
    )

    def handle(self, *args, **options):
        project = ResearchProject.objects.filter(slug=SLUG).first()
        renamed = False

        if project is None:
            # The project predates the widening, so it is carried across under
            # its new name rather than left behind or duplicated.
            project = ResearchProject.objects.filter(slug=OLD_SLUG).first()
            renamed = project is not None

        if project is None:
            self.stderr.write(
                self.style.ERROR(
                    f"No research project with slug '{SLUG}' or '{OLD_SLUG}'. "
                    "Create it in Wagtail first, then run this again."
                )
            )
            return

        project.title = TITLE
        project.slug = SLUG
        project.status = "ongoing"
        project.period = "2026-"
        project.keywords = (
            "particle board, composites, sugarcane bagasse, coconut shell, "
            "recycled plastic, agricultural residue"
        )
        project.summary = SUMMARY
        # An empty gallery renders as nothing, so it is dropped until an author
        # has added photographs rather than left as a blank section.
        project.body = [
            block
            for block in BODY
            if not (block[0] == 'media_gallery' and not block[1]['items'])
        ]
        project.save()

        self.stdout.write(
            self.style.SUCCESS(f"Filled in {project.title} ({SLUG}).")
        )
        if renamed:
            self.stdout.write(
                self.style.WARNING(
                    f"Renamed from '{OLD_SLUG}'. The old URL "
                    f"/research/projects/{OLD_SLUG} no longer resolves; update "
                    "any link that points at it."
                )
            )

        self.stdout.write(
            "\nBefore publishing, an author needs to:"
            "\n  - replace the team roles with real names, once each person"
            "\n    has agreed to appear on a public page"
            "\n  - confirm the period and the activity dates, including when"
            "\n    coconut shell and waste plastics were actually added"
            "\n  - confirm the feedstock table describes what is being tried"
            "\n  - add an Activities gallery after the timeline, showing specimen preparation, pressing and testing"
            "\n  - add references for the reviewed literature\n"
        )
