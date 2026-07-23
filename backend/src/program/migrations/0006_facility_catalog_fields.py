from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("program", "0005_opportunity_announcement_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="facility",
            name="availability_status",
            field=models.CharField(
                choices=[
                    ("available", "Available"),
                    ("new", "New equipment"),
                    ("commissioning", "Commissioning"),
                    ("planned", "Planned"),
                ],
                default="available",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="facility",
            name="reference_url",
            field=models.URLField(
                blank=True,
                help_text="Manufacturer or technical reference page for this machine.",
            ),
        ),
    ]
