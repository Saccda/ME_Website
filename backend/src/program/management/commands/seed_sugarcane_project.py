"""Fill in the Sugarcane Particle Board project page as a worked example.

Written as a draft an author corrects, not as a record of results. Everything
that would need verifying before publication is marked, and the page states no
measured outcome, because none has been supplied. What it does show is the
shape a research project page should take: what the work is for, how it is
being done, who is doing it, and what has actually happened so far.

Names are left as roles. A student's name on a public university page needs
their agreement first, and that is not something a seeding command can give.

    python manage.py seed_sugarcane_project
"""

from django.core.management.base import BaseCommand
from wagtail.rich_text import RichText

from program.models import ResearchProject

SLUG = "sugarcane-particle-board"

SUMMARY = (
    "Cambodia's sugar industry leaves large volumes of bagasse behind after "
    "milling. This project asks whether that residue can be bound into a "
    "particle board strong enough for practical use, and what it takes to get "
    "there."
)

BODY = [
    (
        "paragraph",
        RichText(
            "<p>Bagasse is what remains once sugarcane has been crushed for "
            "juice. It is produced in quantity, it is cheap, and much of it is "
            "burned or left to decay. A material with that profile is worth "
            "examining as an engineering input rather than a waste stream.</p>"
            "<p>The question this project sets out to answer is a narrow one: "
            "can bagasse be combined with a polymer binder to produce a board "
            "whose strength, moisture behaviour and manufacturability are good "
            "enough for real use? A negative answer, clearly demonstrated, "
            "would be a useful result too.</p>"
        ),
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
                        "already reported for agricultural-residue boards, and "
                        "narrow them to those workable with equipment and "
                        "materials available locally."
                    ),
                },
                {
                    "title": "Prepare and characterise the residue",
                    "description": (
                        "Establish a repeatable preparation route -- drying, "
                        "particle size, moisture content -- so that later "
                        "specimens differ by design rather than by accident."
                    ),
                },
                {
                    "title": "Produce trial panels",
                    "description": (
                        "Press specimens across a range of binder ratios and "
                        "compaction conditions, holding everything else fixed."
                    ),
                },
                {
                    "title": "Test and compare",
                    "description": (
                        "Measure mechanical and moisture performance against "
                        "the requirements a usable board would have to meet."
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
                    "period": "Current",
                    "title": "Trial panel production",
                    "detail": (
                        "Producing specimens across a range of binder ratios "
                        "and compaction conditions."
                    ),
                    "status": "current",
                },
                {
                    "period": "Next",
                    "title": "Mechanical and moisture testing",
                    "detail": (
                        "Testing specimens and comparing results against the "
                        "requirements for a usable board."
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
                "the results have been reviewed."
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
            "The material is local, and so is the problem it addresses.</p>"
        ),
    ),
]


class Command(BaseCommand):
    help = (
        "Fill in the Sugarcane Particle Board project as a worked example of "
        "the research page layout. Overwrites that project's body."
    )

    def handle(self, *args, **options):
        try:
            project = ResearchProject.objects.get(slug=SLUG)
        except ResearchProject.DoesNotExist:
            self.stderr.write(
                self.style.ERROR(
                    f"No research project with slug '{SLUG}'. Create it in "
                    "Wagtail first, then run this again."
                )
            )
            return

        project.status = "ongoing"
        project.period = "2026-"
        project.keywords = (
            "sugarcane bagasse, particle board, composites, agricultural residue"
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
        self.stdout.write(
            "\nBefore publishing, an author needs to:"
            "\n  - replace the team roles with real names, once each person"
            "\n    has agreed to appear on a public page"
            "\n  - confirm the period and the activity dates"
            "\n  - add an Activities gallery after the timeline, showing specimen preparation, pressing and testing"
            "\n  - add references for the reviewed literature\n"
        )
