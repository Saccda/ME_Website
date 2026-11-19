from django.db import migrations, models

# The fifteen stories published before the field existed, read and filed one
# by one rather than matched on keywords: "Empowering Innovation Through
# Academic Collaboration" is research and "Strengthening Practical
# Manufacturing Skills" is teaching, and no rule over their titles gets that
# right. Anything published later is filed by its author in Wagtail.
#
# A slug missing from this list keeps the blank default and is listed on
# neither page, which is also what happens if an editor has renamed one.
INITIAL_ALIGNMENT = {
    # M1 -- teaching, learning, and the staff capability behind it.
    "mou-high-school": "teaching",
    "mechanical-engineering-laboratory-open-house": "teaching",
    "me-team-leads-the-first-lex-program": "teaching",
    "focus-area-laboratories-expand-their-teaching-equipment": "teaching",
    "preparing-industry-connected-learning-with-lg-at-campus-iii": "teaching",
    "strengthening-practical-manufacturing-skills-with-vp-start": "teaching",
    "students-train-on-cnc-machines": "teaching",
    "staff-training-on-cnc-milling-machine": "teaching",
    "me-laboratory-welcomes-students-from-battambang-high-school": "teaching",
    # M2 -- research, and the innovation that came out of it into the field.
    "stem-fair": "research",
    "mechanical-engineering-strengthens-its-industry-partnerships": "research",
    "connecting-field-data-with-engineering-decisions": "research",
    "sharing-the-cooling-and-spraying-system-with-communities": "research",
    "installing-cooling-and-spraying-systems-at-two-farms": "research",
    "fairfarms-site-assessment-and-system-design": "research",
}


def file_existing_stories(apps, schema_editor):
    NewsEvent = apps.get_model("program", "NewsEvent")
    for slug, mission in INITIAL_ALIGNMENT.items():
        NewsEvent.objects.filter(slug=slug, mission="").update(mission=mission)


def unfile(apps, schema_editor):
    """Clear only what this migration set, so a re-apply is not destructive."""
    NewsEvent = apps.get_model("program", "NewsEvent")
    for slug, mission in INITIAL_ALIGNMENT.items():
        NewsEvent.objects.filter(slug=slug, mission=mission).update(mission="")


class Migration(migrations.Migration):

    dependencies = [
        ("program", "0030_entrance_prep_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="newsevent",
            name="mission",
            field=models.CharField(
                blank=True,
                choices=[
                    ("teaching", "M1 - Teaching & Learning"),
                    ("research", "M2 - Research & Innovation"),
                    ("both", "Both missions"),
                ],
                help_text=(
                    "Which mission page lists this activity. Leave empty and "
                    "it is listed on neither, which is the right answer for "
                    "an announcement that records no activity."
                ),
                max_length=10,
                verbose_name="Mission alignment",
            ),
        ),
        migrations.RunPython(file_existing_stories, unfile),
    ]
