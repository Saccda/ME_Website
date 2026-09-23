"""Create the article about students training on the CNC machines.

Written from the program's own post about a course activity in which students
were given hands-on time on the CNC machines. The post's social-media framing
-- hashtags, emoji, the closing slogan and a link back to this site -- is left
out: the article is already on the site the link points at, and the site's news
pages are written as plain reporting.

CREATED AS A DRAFT. The post dates the activity only as "one of our previous
course activities", and this site does not publish an article whose date is
unknown: the feeds order by published_at and show only the newest few, so a
guessed date decides which real article gets pushed off the homepage. Supply
the date and the same command dates and publishes it:

    python manage.py seed_cnc_student_training                  # the draft
    python manage.py seed_cnc_student_training --date 2026-03-14

Safe to re-run. The article is matched on its slug and its body is never
rewritten, so anything edited in Wagtail survives; only --date touches an
article that already exists, and only its date and published state.
"""

from datetime import datetime, time

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from program.models import NewsEvent

SLUG = "students-train-on-cnc-machines"
TITLE = "Students Train on CNC Machines"
CATEGORY = "Student Learning"
EXCERPT = (
    "Students worked directly with the CNC machines during a course activity, "
    "following how an engineering drawing becomes a precision part on "
    "computer-controlled equipment."
)

# A story gallery placeholder sits after the opening paragraph, so the
# photographs from the session appear inside the article rather than after it.
# An article with no gallery images drops the block, so the draft reads
# correctly until the pictures are added.
BODY = [
    (
        "paragraph",
        "<p>Students on the Mechanical Engineering program took part in "
        "hands-on training with the CNC machines during a course activity, "
        "working on the equipment rather than only studying it. The session "
        "connected what is taught in class to the machines that modern "
        "manufacturing runs on.</p>",
    ),
    ("story_gallery", {"heading": "From the session", "caption": ""}),
    ("heading", "What CNC machining is"),
    (
        "paragraph",
        "<p>A CNC machine cuts material under computer control, following a "
        "tool path generated from a digital model. Because the movements are "
        "held to programmed dimensions, the same part can be produced again "
        "and again to close tolerances. That repeatability is why the "
        "technology sits at the centre of industrial production.</p>",
    ),
    ("heading", "Where it fits in the program"),
    (
        "paragraph",
        "<p>The activity belongs to the Design and Manufacturing Process area "
        "of focus, where students follow an idea from design through "
        "manufacturing to a finished product. Working on the machine shows "
        "what a drawing has to settle before anything can be cut: dimensions, "
        "tolerances, material, and the order of operations.</p>",
    ),
    (
        "paragraph",
        "<p>As manufacturing and industry develop in Cambodia, familiarity "
        "with computer-controlled production is part of what a mechanical "
        "engineering graduate brings to that work. Training of this kind is "
        "where it starts, while students are still studying.</p>",
    ),
]


class Command(BaseCommand):
    help = (
        "Create the student CNC training article. Created as a draft unless "
        "--date gives the day the activity took place, which publishes it."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            dest="activity_date",
            help=(
                "The date of the activity, as YYYY-MM-DD. Dates the article "
                "and publishes it."
            ),
        )

    def handle(self, *args, activity_date=None, **options):
        published_at = None
        if activity_date:
            try:
                day = datetime.strptime(activity_date, "%Y-%m-%d").date()
            except ValueError:
                raise CommandError(
                    f"--date {activity_date!r} is not a date. Use YYYY-MM-DD."
                )
            # Nine in the morning, the convention the other dated articles use:
            # the day is what the source states, and the hour is not.
            published_at = timezone.make_aware(datetime.combine(day, time(9, 0)))

        existing = NewsEvent.objects.filter(slug=SLUG).first()

        if existing:
            if not published_at:
                self.stdout.write(
                    f"  already on the site, left alone: {SLUG}"
                )
                self.report(existing)
                return
            existing.published_at = published_at
            existing.is_published = True
            existing.save(update_fields=["published_at", "is_published"])
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nDated {published_at.date()} and published: {TITLE}"
                )
            )
            self.report(existing)
            return

        article = NewsEvent.objects.create(
            sort_order=NewsEvent.objects.count() + 1,
            content_type="news",
            category=CATEGORY,
            title=TITLE,
            slug=SLUG,
            excerpt=EXCERPT,
            published_at=published_at or timezone.now(),
            body=BODY,
            is_published=bool(published_at),
        )

        state = "published" if article.is_published else "held as a draft"
        self.stdout.write(self.style.SUCCESS(f"\nCreated and {state}: {TITLE}"))
        self.report(article)

    def report(self, article):
        self.stdout.write(
            "\nIn Wagtail, under Snippets > News & events > "
            f"{article.title}:"
        )
        self.stdout.write(
            "  * Add the lead Image. A card with no picture shows no picture "
            "area at all,\n    which is why this one is not live yet."
        )
        self.stdout.write(
            "  * Add the photographs to Story gallery. They appear where the "
            "Story gallery\n    block sits in the body, and are named after "
            "the article automatically."
        )
        if not article.is_published:
            self.stdout.write(
                "  * Set Published at to the day of the activity and tick "
                "Published,\n    or re-run this with --date YYYY-MM-DD."
            )
