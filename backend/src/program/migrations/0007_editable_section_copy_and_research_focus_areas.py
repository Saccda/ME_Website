from django.db import migrations, models


def copy_research_focus_areas(apps, schema_editor):
    ResearchProject = apps.get_model("program", "ResearchProject")
    for project in ResearchProject.objects.exclude(focus_area_id=None):
        project.focus_areas.add(project.focus_area_id)


def restore_primary_research_focus_area(apps, schema_editor):
    ResearchProject = apps.get_model("program", "ResearchProject")
    for project in ResearchProject.objects.all():
        first_focus_area = project.focus_areas.order_by("sort_order", "pk").first()
        if first_focus_area:
            project.focus_area_id = first_focus_area.pk
            project.save(update_fields=["focus_area"])


def set_focus_facility_headings(apps, schema_editor):
    FocusArea = apps.get_model("program", "FocusArea")
    headings = {
        "DMP": "Design & Manufacturing Lab",
        "TES": "Thermofluid & Energy Systems Lab",
        "MAS": "Mechatronics & Automation Lab",
        "ECM": "Engineering Compliance & Management Lab",
    }
    for code, heading in headings.items():
        FocusArea.objects.filter(code=code).update(facility_heading=heading)


class Migration(migrations.Migration):
    dependencies = [
        ("program", "0006_facility_catalog_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="programsettings",
            name="what_is_me_eyebrow",
            field=models.CharField(
                default="What is mechanical engineering?",
                max_length=120,
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="what_is_me_heading",
            field=models.CharField(
                default="Designed by engineers. Built for the world.",
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="what_is_me_intro",
            field=models.TextField(
                default=(
                    "From drones and vehicles to satellites, robots, and the "
                    "cooling systems behind AI, mechanical engineers shape how "
                    "modern products move, work, and endure."
                )
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="focus_section_eyebrow",
            field=models.CharField(default="Areas of focus", max_length=120),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="focus_section_heading",
            field=models.CharField(
                default="Four paths. One purpose.",
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="focus_section_intro",
            field=models.TextField(
                default=(
                    "Move fluently between theory, simulation, fabrication, "
                    "testing, and responsible engineering practice."
                )
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="why_section_eyebrow",
            field=models.CharField(
                default="Why choose ME at RUPP?",
                max_length=120,
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="why_section_heading",
            field=models.CharField(
                default="Nine reasons. One future-ready program.",
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="why_section_intro",
            field=models.TextField(
                default=(
                    "Our learning model brings technology, social "
                    "responsibility, and active practice together so graduates "
                    "leave ready to contribute from day one."
                )
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="partners_section_eyebrow",
            field=models.CharField(default="Partnership", max_length=120),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="partners_section_heading",
            field=models.CharField(
                default="Education and industry, connected.",
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="programsettings",
            name="partners_section_intro",
            field=models.TextField(
                default=(
                    "Our partnerships connect learning with research, industry "
                    "experience, and job opportunities for ME students."
                )
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="overview_heading",
            field=models.CharField(
                default="Knowledge that becomes engineering ability.",
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="overview_intro",
            field=models.TextField(
                default=(
                    "Connect classroom fundamentals with practical "
                    "investigation, modern tools, teamwork, and evidence-based "
                    "engineering decisions."
                )
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="facility_heading",
            field=models.CharField(
                default="Equipment and facilities",
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="facility_intro",
            field=models.TextField(
                default=(
                    "Learning, research, prototyping, testing, and engineering "
                    "services."
                )
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="curriculum_heading",
            field=models.CharField(
                default="A progressive four-year study path.",
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="curriculum_intro",
            field=models.TextField(
                default=(
                    "Foundation subjects lead to specialist work, integrated "
                    "projects, industry experience, and the final capstone."
                )
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="learning_heading",
            field=models.CharField(
                default="Active learning beyond memorization.",
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="learning_intro",
            field=models.TextField(
                default=(
                    "Activities combine technical knowledge with "
                    "communication, iteration, safety, and reflection."
                )
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="careers_heading",
            field=models.CharField(
                default="Where this focus can take you.",
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="careers_intro",
            field=models.TextField(
                default=(
                    "Graduates can move across technical and leadership roles "
                    "as their experience grows."
                )
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="research_heading",
            field=models.CharField(
                default="Research connected to this focus.",
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="focusarea",
            name="research_intro",
            field=models.TextField(
                default=(
                    "Explore current projects in Research & Innovation for full "
                    "project details and related focus areas."
                )
            ),
        ),
        migrations.RunPython(set_focus_facility_headings, migrations.RunPython.noop),
        migrations.AddField(
            model_name="researchproject",
            name="focus_areas",
            field=models.ManyToManyField(
                blank=True,
                help_text="Select every focus area connected to this project.",
                related_name="research_projects",
                to="program.focusarea",
            ),
        ),
        migrations.RunPython(
            copy_research_focus_areas,
            restore_primary_research_focus_area,
        ),
        migrations.RemoveField(
            model_name="researchproject",
            name="focus_area",
        ),
    ]
