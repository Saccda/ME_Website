from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("program", "0007_editable_section_copy_and_research_focus_areas"),
    ]

    operations = [
        migrations.AddField(
            model_name="programsettings",
            name="research_hero_eyebrow",
            field=models.CharField(default="Research at ME RUPP", max_length=120),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_hero_title",
            field=models.CharField(
                default="Engineering research at the interface of ideas",
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_hero_description",
            field=models.TextField(
                default=(
                    "Our work connects design, energy, automation, and responsible "
                    "engineering to practical challenges in Cambodia and beyond."
                )
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_quote",
            field=models.TextField(
                default=(
                    "Mechanical engineering research is strongest where disciplines "
                    "meet and useful solutions begin to take shape."
                )
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_quote_attribution",
            field=models.CharField(
                default="Design · Energy · Automation · Responsible engineering",
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_areas_eyebrow",
            field=models.CharField(default="Explore research", max_length=120),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_areas_heading",
            field=models.CharField(
                default="Investigate our four research areas", max_length=220
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_areas_intro",
            field=models.TextField(
                default=(
                    "Each area organizes expertise without limiting collaboration "
                    "across disciplines."
                )
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_projects_eyebrow",
            field=models.CharField(default="Current research", max_length=120),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_projects_heading",
            field=models.CharField(
                default="Explore current research projects", max_length=220
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_projects_intro",
            field=models.TextField(
                default=(
                    "Open a project through its primary area to see its full context "
                    "and connected disciplines."
                )
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_collaboration_eyebrow",
            field=models.CharField(default="Research collaboration", max_length=120),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_collaboration_heading",
            field=models.CharField(
                default="Good research grows through shared expertise.", max_length=220
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_area_projects_eyebrow",
            field=models.CharField(default="Current investigations", max_length=120),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_area_projects_intro",
            field=models.TextField(
                default=(
                    "Projects may also appear in another research area when the work "
                    "depends on shared expertise."
                )
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_boundaries_eyebrow",
            field=models.CharField(default="Connected by the problem", max_length=120),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="research_boundaries_heading",
            field=models.CharField(
                default="Research areas guide collaboration. They do not limit it.",
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="research_question",
            field=models.TextField(
                blank=True,
                help_text=(
                    "The guiding research question shown on this area's research page."
                ),
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="research_overview",
            field=models.TextField(
                blank=True,
                help_text=(
                    "Introduces what this area investigates on its research page."
                ),
            ),
        ),
        migrations.AlterField(
            model_name="focusareadetailitem",
            name="item_type",
            field=models.CharField(
                choices=[
                    ("outcome", "Learning outcome"),
                    ("activity", "Learning activity"),
                    ("career", "Career pathway"),
                    ("theme", "Research theme"),
                ],
                max_length=20,
            ),
        ),
    ]
