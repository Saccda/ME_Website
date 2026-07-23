from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("program", "0003_programsettings_social_urls"),
    ]

    operations = [
        migrations.CreateModel(
            name="Opportunity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sort_order", models.PositiveIntegerField(db_index=True, default=0)),
                ("title", models.CharField(max_length=220)),
                ("slug", models.SlugField(max_length=240, unique=True)),
                (
                    "opportunity_type",
                    models.CharField(
                        choices=[
                            ("job", "Job"),
                            ("internship", "Internship"),
                            ("scholarship", "Scholarship"),
                            ("training", "Training"),
                        ],
                        default="job",
                        max_length=20,
                    ),
                ),
                ("summary", models.TextField()),
                ("body", wagtail.fields.RichTextField(blank=True)),
                ("location", models.CharField(blank=True, max_length=180)),
                ("application_deadline", models.DateField(blank=True, null=True)),
                ("application_url", models.URLField(blank=True)),
                ("published_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_published", models.BooleanField(default=False)),
                (
                    "is_featured",
                    models.BooleanField(
                        default=False,
                        help_text="Prioritize this announcement on the homepage.",
                    ),
                ),
                (
                    "focus_areas",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Focus areas most relevant to this opportunity.",
                        related_name="opportunities",
                        to="program.focusarea",
                    ),
                ),
                (
                    "partner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="opportunities",
                        to="program.partner",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Opportunities",
                "ordering": ("sort_order", "pk"),
            },
        ),
    ]
