from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from program.models import FocusArea, NewsEvent, ProgramSettings


# Starter entries for the homepage news and events bands.
#
# Offsets are days from the run rather than fixed dates, so a freshly seeded site
# always has events that are genuinely still to come. These are placeholders for
# authors to rewrite in Wagtail, so they are created with get_or_create: running
# this command again must never overwrite an edit someone has made.
NEWS_ITEMS = [
    (
        "A new academic year begins in the ME laboratories",
        -10,
        "Teaching resumes across the four focus-area laboratories, with "
        "first-year students starting their introduction to workshop practice "
        "and laboratory safety.",
        "DMP",
    ),
    (
        "Focus-area laboratories expand their teaching equipment",
        -45,
        "Additional equipment is being commissioned for practical teaching, "
        "giving students more hands-on time with the systems they study.",
        None,
    ),
    (
        "Mechanical Engineering strengthens its industry partnerships",
        -90,
        "The programme continues to develop its relationships with industry, "
        "supporting internships, capstone projects, and applied research.",
        "MAS",
    ),
]

EVENT_ITEMS = [
    (
        "Mechanical Engineering laboratory open house",
        45,
        "Prospective students and their families are invited to tour the "
        "focus-area laboratories and meet the teaching staff.",
        None,
    ),
    (
        "Industry and academic partnership day",
        80,
        "Partners and programme staff meet to review internship placements "
        "and capstone project briefs for the year ahead.",
        "ECM",
    ),
    (
        "Student capstone project showcase",
        120,
        "Final-year students present their capstone work to staff, partners, "
        "and the wider faculty.",
        "TES",
    ),
]


def seed_news_events():
    """Create the starter entries, leaving any that already exist untouched.

    Images are taken from records already in the database rather than from the
    assets directory, so this can run inside the deployed container, where the
    prepared assets are not present.

    Returns the number of entries created.
    """
    focus_images = {
        area.code: area.image for area in FocusArea.objects.all() if area.image
    }
    settings_object = ProgramSettings.objects.first()
    default_image = settings_object.hero_image if settings_object else None
    now = timezone.now()
    created_count = 0

    def create(index, content_type, title, offset, excerpt, focus_code, is_event):
        nonlocal created_count
        moment = now + timedelta(days=offset)
        _, created = NewsEvent.objects.get_or_create(
            slug=slugify(title),
            defaults={
                "sort_order": index,
                "content_type": content_type,
                "title": title,
                "excerpt": excerpt,
                "image": focus_images.get(focus_code, default_image),
                "event_date": moment if is_event else None,
                "published_at": now if is_event else moment,
                "is_published": True,
            },
        )
        if created:
            created_count += 1

    for index, (title, offset, excerpt, focus_code) in enumerate(NEWS_ITEMS, start=1):
        create(index, "news", title, offset, excerpt, focus_code, False)

    for index, (title, offset, excerpt, focus_code) in enumerate(
        EVENT_ITEMS, start=len(NEWS_ITEMS) + 1
    ):
        create(index, "event", title, offset, excerpt, focus_code, True)

    return created_count


class Command(BaseCommand):
    help = (
        "Create starter homepage news and events entries. Safe to re-run: "
        "existing entries are never modified."
    )

    def handle(self, *args, **options):
        created = seed_news_events()
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {created} news/event entries "
                f"({NewsEvent.objects.count()} total)."
            )
        )
