from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("program", "0004_opportunity"),
    ]

    operations = [
        migrations.AddField(
            model_name="opportunity",
            name="announcement_image",
            field=models.ForeignKey(
                blank=True,
                help_text=(
                    "Upload the partner's hiring poster or announcement artwork. "
                    "A landscape 3:2 image is recommended."
                ),
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.image",
            ),
        ),
    ]
