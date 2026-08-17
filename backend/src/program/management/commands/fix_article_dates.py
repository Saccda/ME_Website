"""Repair the publication dates the article-bank seeding got wrong.

The first seeding run stamped every article whose activity date the source
document left unconfirmed with the run time. Ten articles therefore claimed to
have been published today, which put them above every real article on the site
and pushed the program's own recent news off both the homepage band and the
news listing -- neither of which shows more than a handful, ordered by
published_at.

This command fixes that in the two honest ways available:

  * articles the source document does date are given that date;
  * articles it does not are held as drafts, which is what the document's own
    publication check asks for. They keep their body and stay in Wagtail,
    ready to publish the moment an author supplies the date.

Only bank slugs are touched, so authored articles are never affected. Safe to
re-run.

    python manage.py fix_article_dates
"""

from datetime import date, datetime, time

from django.core.management.base import BaseCommand
from django.utils import timezone

from program.models import NewsEvent

# Dates the source document states. Where it gives only a month or a range, the
# end of that period is used: it is the earliest date the article cannot be
# claiming too early, and it keeps the ordering honest without inventing a day.
CONFIRMED = {
    # "Construction review recorded on 13 May 2026"
    "planning-mechanical-engineering-learning-spaces-for-campus-iii": date(2026, 5, 13),
    # "Development status recorded in June 2026"
    "developing-an-additive-manufacturing-system": date(2026, 6, 30),
    # "May - June 2026"
    "mex-learning-journey-hands-on-automation": date(2026, 6, 30),
    # The article cites the 4 August 2026 session by name.
    "tuesday-weekly-seminar-technical-exchange": date(2026, 8, 4),
}

# "Activity date not provided" in the source document. Held back rather than
# dated, because any date here would be invented.
#
# staff-training-on-cnc-milling-machine is in this list even though the
# document dates the original E-Day 2025 framing: that framing was dropped when
# the article was reframed as staff training, so the date no longer describes
# what the article is about.
UNDATED = (
    "designing-a-safer-water-booster-pump-control-system",
    "connecting-field-data-with-engineering-decisions",
    "staff-training-on-cnc-milling-machine",
    "strengthening-practical-manufacturing-skills-with-vp-start",
    "me-laboratory-welcomes-students-from-battambang-high-school",
    "preparing-industry-connected-learning-with-lg-at-campus-iii",
)

# Estimated, and approved as estimates by the author. Left alone: they already
# carry dates that place them correctly, and they are flagged as estimates.
ESTIMATED = (
    "fairfarms-site-assessment-and-system-design",
    "installing-cooling-and-spraying-systems-at-two-farms",
    "sharing-the-cooling-and-spraying-system-with-communities",
)


class Command(BaseCommand):
    help = (
        "Correct the article-bank publication dates: apply the dates the "
        "source document states, and hold undated articles as drafts. Only "
        "touches bank articles."
    )

    def handle(self, *args, **options):
        dated, held, missing = [], [], []

        for slug, when in CONFIRMED.items():
            article = NewsEvent.objects.filter(slug=slug).first()
            if article is None:
                missing.append(slug)
                continue
            article.published_at = timezone.make_aware(
                datetime.combine(when, time(9, 0))
            )
            article.is_published = True
            article.save(update_fields=["published_at", "is_published"])
            dated.append((slug, when))

        for slug in UNDATED:
            article = NewsEvent.objects.filter(slug=slug).first()
            if article is None:
                missing.append(slug)
                continue
            if article.is_published:
                article.is_published = False
                article.save(update_fields=["is_published"])
            held.append(slug)

        for slug, when in sorted(dated, key=lambda pair: pair[1]):
            self.stdout.write(f"  dated {when}  {slug}")
        for slug in held:
            self.stdout.write(f"  held as draft   {slug}")
        for slug in missing:
            self.stdout.write(
                self.style.WARNING(f"  not on the site, skipped: {slug}")
            )

        visible = NewsEvent.objects.filter(
            is_published=True, published_at__lte=timezone.now()
        ).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"\nDated {len(dated)}, held {len(held)} as drafts. "
                f"{visible} article(s) now visible on the site."
            )
        )
        self.stdout.write(
            "\nThe held articles need an activity date before they go back up."
            "\nAdd the date in Wagtail and tick Published, or send the dates"
            "\nand they can be applied in one pass.\n"
        )
