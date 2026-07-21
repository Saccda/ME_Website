from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("program", "0002_course_focus_areas_facility_focus_areas_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="programsettings",
            name="linkedin_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="telegram_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="youtube_url",
            field=models.URLField(blank=True),
        ),
    ]
