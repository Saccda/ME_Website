from django.db import migrations, models

# The program revised its missions from two to three in November 2026, and
# reworded the two it kept. Both are carried here so a running site picks up
# the approved text on deploy rather than waiting for someone to retype it
# into Wagtail.
OLD_MISSION_ONE = (
    "To provide a modern mechanical engineering education by infusing social "
    "engagement and technology into educational activity for an effective "
    "educational program."
)
OLD_MISSION_TWO = (
    "To collaborate with university partners on mechanical engineering to "
    "enforce proactive research activities that lead to an advancement of "
    "research and innovation."
)
NEW_MISSION_ONE = (
    "Equipping students with rigorous engineering fundamentals, practical "
    "hands-on competence, ethical values, and lifelong learning attitudes "
    "across all ME primary focuses."
)
NEW_MISSION_TWO = (
    "Conducting high-quality, industry-relevant research and technological "
    "innovation to advance sustainable industrial productivity and "
    "engineering practices."
)

# The six activities that change hands, as slug -> (what 0031 filed it as,
# where it goes now). Nine others keep the filing they have.
#
# M1 is now specifically about equipping students, so an open house or a
# school visit is no longer teaching: it is M3, the mission about working
# with people outside the program, and so is maintaining a system on a
# partner's farm. Staff training stays in M1, because its whole purpose is
# the teaching it makes possible.
REFILED = {
    "mechanical-engineering-laboratory-open-house": ("teaching", "society"),
    "me-laboratory-welcomes-students-from-battambang-high-school": (
        "teaching",
        "society",
    ),
    "mou-high-school": ("teaching", "society"),
    "focus-area-laboratories-expand-their-teaching-equipment": (
        "teaching",
        "society",
    ),
    "mechanical-engineering-strengthens-its-industry-partnerships": (
        "research",
        "society",
    ),
    "sharing-the-cooling-and-spraying-system-with-communities": (
        "research",
        "society",
    ),
}


def adopt_revised_missions(apps, schema_editor):
    """Replace the two superseded statements, and nothing an editor has
    touched: a value that is no longer the old wording is somebody's edit and
    is left where it is."""
    ProgramSettings = apps.get_model("program", "ProgramSettings")
    ProgramSettings.objects.filter(mission_one=OLD_MISSION_ONE).update(
        mission_one=NEW_MISSION_ONE
    )
    ProgramSettings.objects.filter(mission_two=OLD_MISSION_TWO).update(
        mission_two=NEW_MISSION_TWO
    )


def restore_superseded_missions(apps, schema_editor):
    ProgramSettings = apps.get_model("program", "ProgramSettings")
    ProgramSettings.objects.filter(mission_one=NEW_MISSION_ONE).update(
        mission_one=OLD_MISSION_ONE
    )
    ProgramSettings.objects.filter(mission_two=NEW_MISSION_TWO).update(
        mission_two=OLD_MISSION_TWO
    )


def refile_activities(apps, schema_editor):
    """Move the six that change hands.

    Matched on the filing 0031 gave them, so an editor who has already filed
    one differently keeps their answer.
    """
    NewsEvent = apps.get_model("program", "NewsEvent")
    for slug, (previous, now) in REFILED.items():
        NewsEvent.objects.filter(slug=slug, mission=previous).update(mission=now)


def unfile_activities(apps, schema_editor):
    NewsEvent = apps.get_model("program", "NewsEvent")
    for slug, (previous, now) in REFILED.items():
        NewsEvent.objects.filter(slug=slug, mission=now).update(mission=previous)


class Migration(migrations.Migration):

    dependencies = [
        ("program", "0031_newsevent_mission"),
    ]

    operations = [
        migrations.AddField(
            model_name="programsettings",
            name="mission_three",
            field=models.TextField(
                default=(
                    "Collaborating actively with industry, government, and local "
                    "communities to develop practical, resilient engineering "
                    "solutions."
                ),
                verbose_name="Mission 3 - Societal Engagement",
            ),
        ),
        migrations.AlterField(
            model_name="programsettings",
            name="mission_one",
            field=models.TextField(
                default=(
                    "Equipping students with rigorous engineering fundamentals, "
                    "practical hands-on competence, ethical values, and lifelong "
                    "learning attitudes across all ME primary focuses."
                ),
                verbose_name="Mission 1 - Teaching & Learning",
            ),
        ),
        migrations.AlterField(
            model_name="programsettings",
            name="mission_two",
            field=models.TextField(
                default=(
                    "Conducting high-quality, industry-relevant research and "
                    "technological innovation to advance sustainable industrial "
                    "productivity and engineering practices."
                ),
                verbose_name="Mission 2 - Applied Research & Innovation",
            ),
        ),
        migrations.AlterField(
            model_name="newsevent",
            name="mission",
            field=models.CharField(
                blank=True,
                choices=[
                    ("teaching", "M1 - Teaching & Learning"),
                    ("research", "M2 - Applied Research & Innovation"),
                    ("society", "M3 - Societal Engagement"),
                ],
                help_text=(
                    "Which mission page lists this activity. Leave empty and "
                    "it is listed on none of them, which is the right answer for "
                    "an announcement that records no activity."
                ),
                max_length=10,
                verbose_name="Mission alignment",
            ),
        ),
        migrations.RunPython(adopt_revised_missions, restore_superseded_missions),
        migrations.RunPython(refile_activities, unfile_activities),
    ]
