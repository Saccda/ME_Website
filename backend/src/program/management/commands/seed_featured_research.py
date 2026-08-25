"""Draft the landing-page story for the cooling and spraying project.

A draft an author corrects, not a finished claim. Everything here is drawn
from what the ME team has described and from the FarmOS interface itself; no
figure is invented, because none has been supplied. There is deliberately no
"30% less water" or "twice the yield" -- a number on a landing page is the
first thing a reader checks and the first thing that discredits the rest.

Nothing asserts that the system is running right now. FarmOS reports itself
offline between deployments, and the landing page must not claim otherwise.

    python manage.py seed_featured_research
"""

from django.core.management.base import BaseCommand

from program.models import ResearchProject

SLUG = "automated-cooling-spraying-system"

SUMMARY = (
    "A Kampot pepper farm is cooled and irrigated on judgement: somebody "
    "decides when to run the pump. The ME team built the equipment that does "
    "it on sensor readings instead, and the software that runs it."
)

STORY = [
    {
        "title": "The problem, on a farm in Kampot",
        "description": (
            "Cooling and spraying were done by hand, on judgement. Too little "
            "and the crop suffers; too much wastes water and power; and either "
            "way nobody finds out until the damage shows."
        ),
    },
    {
        "title": "The equipment, built in the ME laboratory",
        "description": (
            "Temperature and humidity sensors, a spray pump, a cooling loop, "
            "relays and a control cabinet, powered from solar. Designed, "
            "assembled and commissioned by the ME team with Solar Green Energy "
            "Cambodia."
        ),
    },
    {
        "title": "FarmOS, the software that runs it",
        "description": (
            "A web platform the team wrote: temperature and humidity plotted "
            "over time, thresholds a farm owner sets themselves, direct "
            "control of each relay, an alert log and a history browser. "
            "Mechanical engineering here includes writing the software."
        ),
    },
    {
        "title": "Installed, and handed over",
        "description": (
            "Running at two farms in Kampot, with the work shared at community "
            "sessions organised by ADB and PIN. It left the laboratory, which "
            "is the part that counts."
        ),
    },
]


class Command(BaseCommand):
    help = (
        "Draft the landing-page story for the cooling and spraying project and "
        "feature it. Overwrites that project's landing story."
    )

    def handle(self, *args, **options):
        project = ResearchProject.objects.filter(slug=SLUG).first()
        if project is None:
            self.stderr.write(
                self.style.ERROR(
                    f"No research project with slug '{SLUG}'. Create it in "
                    "Wagtail first, then run this again."
                )
            )
            return

        # Only one project leads the landing page, so featuring this one
        # unfeatures whatever held the slot before.
        ResearchProject.objects.exclude(pk=project.pk).update(is_featured=False)

        project.is_featured = True
        project.summary = SUMMARY
        project.platform_url = "https://farmos-mechanicalengineering.com/"
        project.platform_label = "FarmOS — sign-in is for farm owners"
        project.landing_story = [
            (
                "steps",
                {"heading": "How it was done", "steps": STORY},
            )
        ]
        project.save()

        self.stdout.write(
            self.style.SUCCESS(f"Featured {project.title} on the landing page.")
        )
        self.stdout.write(
            "\nThe words are a draft. Correct them in Wagtail under Snippets >"
            "\nResearch projects > Landing page, and add the two pictures:"
            "\n  - Showcase image: the FarmOS dashboard. It is the one thing a"
            "\n    reader will not expect from a mechanical engineering program,"
            "\n    so it should be the picture the band leads with."
            "\n  - Project image: the installation itself -- cabinet, tanks,"
            "\n    pipework."
            "\n\nNo performance figure is claimed anywhere. Do not add one"
            "\nwithout a measurement behind it.\n"
        )
