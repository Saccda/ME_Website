"""Name the gallery photos that still carry the file name a device gave them.

Saving a story in Wagtail now names its device-named gallery photos after the
story. This does the same, once, for the galleries built before that:

    python manage.py name_gallery_photos --dry-run   # list the new names
    python manage.py name_gallery_photos             # apply them

Only titles that look like a phone, camera or app file name are touched -- see
program/photo_titles.py for the patterns. A name someone typed is left alone,
and each file keeps its original name in storage, so nothing is lost. Safe to
re-run: a photo that has been named no longer looks like a device's file name.
"""

from django.core.management.base import BaseCommand

from program.models import NewsEvent
from program.photo_titles import name_story_gallery


class Command(BaseCommand):
    help = (
        "Name story gallery photos whose titles are still a device's file "
        "name after their story, numbered in gallery order."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List the new names without saving them.",
        )

    def handle(self, *args, dry_run=False, **options):
        renamed = 0

        for story in NewsEvent.objects.order_by("title"):
            changes = name_story_gallery(story, dry_run=dry_run)
            if not changes:
                continue
            self.stdout.write(f"\n{story.title}")
            for old, new in changes:
                self.stdout.write(f"  {old}  ->  {new}")
            renamed += len(changes)

        verb = "Would rename" if dry_run else "Renamed"
        self.stdout.write(self.style.SUCCESS(f"\n{verb} {renamed} photo(s)."))
