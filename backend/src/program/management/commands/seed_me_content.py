from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from wagtail.images import get_image_model
from wagtail.models import Site

from program.models import (
    Course,
    CurriculumYear,
    Facility,
    FocusArea,
    FocusAreaDetailItem,
    Partner,
    ProgramSettings,
    ResearchProject,
    WhyChooseItem,
)


WHY_ITEMS = [
    (
        "Aligned with AUN–QA criteria",
        "Program quality is guided by recognized regional quality-assurance criteria.",
        "why/01-aunqa.webp",
        "logo",
    ),
    (
        "Job-ready Knowledge, Experiences, Skills and Attitudes",
        "Build practical knowledge, experience, technical skills, and professional attitudes through real engineering work.",
        "why/02-job-ready.webp",
        "photo",
    ),
    (
        "Strong Collaboration with Industrial & Academic Partner",
        "Learn through active relationships with industrial and academic partners, from joint projects to professional exchange.",
        "why/03-collaboration.webp",
        "photo",
    ),
    (
        "Member of CDIO Community",
        "Connect ideas to working outcomes by learning to conceive, design, implement, and operate real systems.",
        "why/04-cdio.webp",
        "logo",
    ),
    (
        "Infused Technology into Teaching & Learning",
        "Use modern laboratory equipment, digital tools, and manufacturing technology throughout the learning experience.",
        "why/05-technology.webp",
        "photo",
    ),
    (
        "On par with emerging trends and Technologies: ML, AI, EV",
        "Explore machine learning, artificial intelligence, electric vehicles, automation, and Industry 4.0 applications.",
        "why/06-emerging-tech.webp",
        "photo",
    ),
    (
        "Adopt Cambodia FutureFit Framework",
        "Develop adaptable, resilient, and socially responsible engineering capabilities grounded in Cambodia’s future needs.",
        "why/07-futurefit.webp",
        "logo",
    ),
    (
        "Social Engagement and Community Services",
        "Connect engineering education with community service, empathy, teamwork, and meaningful social contribution.",
        "why/08-social-engagement.webp",
        "logo",
    ),
    (
        "Active Experiential Learning beyond memorization",
        "Learn by building, testing, discussing, and improving through laboratories, workshops, site visits, and team projects.",
        "why/09-active-learning.webp",
        "photo",
    ),
]

FOCUS_AREAS = [
    (
        "DMP",
        "Design and Manufacturing Process",
        "Learn how ideas become real products — from creative design to modern manufacturing methods that shape everything we use.",
        "#061b2b",
        "focus-dmp.png",
    ),
    (
        "TES",
        "Thermofluid and Energy System",
        "Engineer systems to utilize energy through generation, transfer, and storage — from cooling and heating to sustainable energy for the future.",
        "#e6ad38",
        "focus-tes.png",
    ),
    (
        "MAS",
        "Mechatronic and Automation System",
        "Discover how mechanical, electrical, and computer systems work together — building smart machines and automation for Industry 4.0.",
        "#1667b1",
        "focus-mas.png",
    ),
    (
        "ECM",
        "Engineering Compliance and Management",
        "Gain skills in safety, standards, and project management — ensuring engineering solutions are reliable, efficient, and ready for the real world.",
        "#3e8b56",
        "focus-ecm.png",
    ),
]

CURRICULUM = [
    (
        1,
        "Foundations & discovery",
        36,
        "Develop mathematical confidence, engineering intuition, and essential workshop skills.",
        [
            ("MTH 101", "Calculus for Engineers I", 5),
            ("PHY 101", "Engineering Physics I", 5),
            ("ME 103", "Engineering Drawing & CAD", 4),
            ("ME 105", "Introduction to Mechanical Engineering", 3),
            ("ME 107", "Workshop Practice & Safety", 4),
            ("ENG 101", "Academic English for Engineers", 3),
            ("CHM 101", "General Chemistry", 4),
            ("GEN 101", "Khmer Culture & Society", 3),
        ],
    ),
    (
        2,
        "Core engineering systems",
        36,
        "Connect mechanics, materials, thermofluids, electronics, and computation through lab-based study.",
        [
            ("MTH 203", "Engineering Mathematics III", 4),
            ("ME 211", "Thermodynamics I", 4),
            ("ME 213", "Mechanics of Materials", 4),
            ("ME 215", "Dynamics of Machinery", 4),
            ("ME 217", "Fluid Mechanics", 4),
            ("ME 219", "Materials & Manufacturing", 4),
            ("EE 201", "Electrical Systems for ME", 4),
            ("ME 221", "Computational Methods", 4),
        ],
    ),
    (
        3,
        "Integration & specialization",
        35,
        "Choose a focus area while integrating analysis, experimentation, design, and control.",
        [
            ("ME 311", "Heat Transfer", 4),
            ("ME 313", "Machine Design", 4),
            ("ME 315", "Control Systems", 4),
            ("ME 317", "Mechatronics Laboratory", 4),
            ("ME 319", "Numerical Simulation", 4),
            ("ME 3E1", "Focus Area Elective I", 4),
            ("ME 3E2", "Focus Area Elective II", 4),
            ("GEN 301", "Engineering Economics", 3),
        ],
    ),
    (
        4,
        "Practice, leadership & impact",
        36,
        "Apply the full engineering process through professional practice, research, and a major capstone project.",
        [
            ("ME 401", "Capstone Design Project I", 5),
            ("ME 402", "Capstone Design Project II", 5),
            ("ME 403", "Industrial Internship", 6),
            ("ME 405", "Applied Research Methods", 3),
            ("ME 4E1", "Focus Area Elective III", 4),
            ("ME 4E2", "Focus Area Elective IV", 4),
            ("ME 411", "Sustainable Engineering", 3),
            ("GEN 401", "Leadership & Professional Ethics", 3),
        ],
    ),
]

RESEARCH = [
    (
        "Metal Recycling",
        ("DMP",),
        "Exploring practical processes for recovering, sorting, and reusing metal resources to support more sustainable manufacturing.",
    ),
    (
        "Automated Cooling & Spraying System",
        ("TES", "MAS"),
        "Developing sensor-based cooling and spraying controls for more consistent, efficient environmental management.",
    ),
    (
        "Sugarcane Particle Board",
        ("DMP", "ECM"),
        "Investigating sugarcane residue as a useful raw material for lower-impact engineered particle board.",
    ),
    (
        "Non-Intrusive Load Monitoring System",
        ("TES", "MAS"),
        "Using electrical measurements and intelligent analysis to identify appliance-level energy use without individual sensors.",
    ),
]

PARTNERS = [
    ("CJDM Digitalized Manufacturing", "industry", "partners/cjdm.png"),
    ("Dynamic Engineering Steels", "industry", "partners/des.jpg"),
    ("GGEAR Group", "industry", "partners/ggear.png"),
    ("Legrand", "industry", "partners/legrand.png"),
    ("LG", "industry", "partners/lg.png"),
    ("Université Sorbonne Paris Nord", "academic", "partners/universite-sorbonne-paris-nord.jpg"),
    ("Saint-Gobain", "industry", "partners/saint-gobain.png"),
    ("Singapore Polytechnic", "academic", "partners/singapore-polytechnic.png"),
    ("Solar Green Energy Cambodia", "industry", "partners/soge.png"),
    ("VP.Start", "industry", "partners/vp-start.png"),
]

FOCUS_COURSE_CODES = {
    "DMP": {
        "ME 103",
        "ME 107",
        "ME 213",
        "ME 219",
        "ME 313",
        "ME 319",
        "ME 3E1",
        "ME 3E2",
        "ME 401",
        "ME 402",
        "ME 403",
        "ME 4E1",
        "ME 4E2",
    },
    "TES": {
        "PHY 101",
        "ME 211",
        "ME 217",
        "ME 311",
        "ME 319",
        "ME 3E1",
        "ME 3E2",
        "ME 401",
        "ME 402",
        "ME 403",
        "ME 4E1",
        "ME 4E2",
        "ME 411",
    },
    "MAS": {
        "ME 105",
        "ME 215",
        "EE 201",
        "ME 221",
        "ME 315",
        "ME 317",
        "ME 319",
        "ME 3E1",
        "ME 3E2",
        "ME 401",
        "ME 402",
        "ME 403",
        "ME 4E1",
        "ME 4E2",
    },
    "ECM": {
        "ME 107",
        "GEN 301",
        "ME 401",
        "ME 402",
        "ME 403",
        "ME 405",
        "ME 411",
        "GEN 401",
        "ME 4E1",
        "ME 4E2",
    },
}

FOCUS_DETAIL_ITEMS = {
    "DMP": {
        "outcome": [
            ("Design for manufacture", "Translate user needs into manufacturable components, assemblies, drawings, and specifications."),
            ("Digital engineering workflow", "Use CAD, simulation, CAM, and data to move confidently from concept to production."),
            ("Materials and process selection", "Choose suitable materials and manufacturing processes using performance, cost, and sustainability criteria."),
            ("Quality through testing", "Measure, inspect, test, and improve products using evidence from the workshop and laboratory."),
        ],
        "activity": [
            ("CAD-to-component design sprint", "Develop a part from an initial brief, validate it digitally, and prepare it for manufacture."),
            ("CNC and workshop practice", "Set up machining operations while applying safe working methods and process controls."),
            ("Materials testing investigation", "Compare material behavior and connect test results to practical design decisions."),
            ("Industry design challenge", "Respond to a partner problem through teamwork, prototyping, review, and iteration."),
        ],
        "career": [
            ("Design Engineer", "Develop products, mechanisms, and production-ready engineering documentation."),
            ("Manufacturing Engineer", "Improve processes, tooling, quality, efficiency, and production capability."),
            ("Process Engineer", "Design and optimize reliable industrial processes."),
            ("Product Engineer", "Guide a product from concept and testing through manufacture and improvement."),
        ],
    },
    "TES": {
        "outcome": [
            ("Thermal system analysis", "Model heat, work, energy conversion, and system performance using engineering fundamentals."),
            ("Fluid and heat-transfer design", "Evaluate flow, pressure, cooling, heating, and heat-exchanger behavior."),
            ("Energy performance improvement", "Measure consumption, identify losses, and propose practical efficiency improvements."),
            ("Sustainable energy integration", "Assess renewable generation, storage, and responsible energy use for Cambodian needs."),
        ],
        "activity": [
            ("Thermal and fluid laboratory", "Test real systems, compare measurements with theory, and communicate uncertainty."),
            ("Cooling-system build", "Design and test a controlled cooling or spraying solution for a practical application."),
            ("Campus energy audit", "Collect energy-use evidence and turn it into prioritized improvement recommendations."),
            ("Renewable-energy field study", "Evaluate operating conditions, performance, maintenance, and community context on site."),
        ],
        "career": [
            ("Energy Engineer", "Improve energy generation, conversion, efficiency, and sustainability."),
            ("Power Engineer", "Support reliable energy and power systems across facilities and industry."),
            ("HVAC Engineer", "Design and manage heating, ventilation, refrigeration, and cooling systems."),
            ("Plant Engineer", "Operate and improve complex thermal, fluid, and utility systems."),
        ],
    },
    "MAS": {
        "outcome": [
            ("Integrated system design", "Combine mechanical, electrical, sensing, control, and software elements into working machines."),
            ("Automation and control", "Develop control logic and tune automated systems for reliable performance."),
            ("Sensors and intelligent data", "Acquire, interpret, and use machine data for monitoring and decision-making."),
            ("Robotics and Industry 4.0", "Apply robotics, artificial vision, connected systems, and digital manufacturing concepts."),
        ],
        "activity": [
            ("Sensor-and-actuator prototype", "Build a closed-loop system that senses its environment and responds predictably."),
            ("Robot vision programming", "Configure a vision-assisted robot task and improve its accuracy through testing."),
            ("PLC automation challenge", "Create, document, and troubleshoot an industrial sequence using safe automation practice."),
            ("EV control experiment", "Investigate electric mobility subsystems, control behavior, and system integration."),
        ],
        "career": [
            ("Mechatronics Engineer", "Create integrated electromechanical products and intelligent machines."),
            ("Automation Engineer", "Design, program, commission, and improve automated systems."),
            ("Control Systems Engineer", "Develop reliable control strategies for machines, vehicles, and processes."),
            ("Systems Engineer", "Coordinate complex technical requirements, interfaces, verification, and delivery."),
        ],
    },
    "ECM": {
        "outcome": [
            ("Standards and compliance", "Interpret relevant standards and translate them into clear engineering requirements."),
            ("Safety and risk management", "Identify hazards, evaluate risk, and design practical controls throughout a project."),
            ("Quality and reliability", "Plan inspection, verification, documentation, and continuous improvement activities."),
            ("Engineering project leadership", "Balance scope, time, cost, people, quality, and professional responsibility."),
        ],
        "activity": [
            ("Safety and risk assessment", "Inspect an engineering activity and prepare a practical hierarchy of controls."),
            ("Standards compliance review", "Assess a design or process against selected requirements and document evidence."),
            ("Project planning simulation", "Build a delivery plan with resources, schedule, risk, quality, and stakeholder actions."),
            ("Industry quality audit", "Observe a real process and report improvement opportunities using structured evidence."),
        ],
        "career": [
            ("Project Engineer", "Coordinate technical work, resources, risk, quality, and stakeholder delivery."),
            ("Quality Engineer", "Build systems that prevent defects and improve process capability."),
            ("Compliance Engineer", "Ensure products and operations meet standards, regulations, and documented requirements."),
            ("Facility Engineer", "Manage safe, reliable, and efficient engineering services and assets."),
        ],
    },
}

FOCUS_EQUIPMENT = [
    ("Excetek V400G Plus Wire-Cut EDM", "Cut complex profiles in electrically conductive materials through controlled wire electrical-discharge machining.", "https://www.excetek.com/shop/v400g-plus-17#attr=", "available", ("DMP",)),
    ("Rownd Desktop CNC Lathe", "Support compact CNC turning, small-part production, CAD/CAM practice, and manufacturing-process training.", "https://rowndprecision.com/en-us/products/rownd-desktop-cnc-lathe-compact-modular-high-precision-3", "available", ("DMP",)),
    ("DMC2 Mini CNC", "Provide a compact CNC platform for machining practice, prototyping, setup, tooling, and process planning.", "https://shariffdmc.com/product/dmc2-mini-cnc/", "available", ("DMP",)),
    ("Carbolite HTF High-Temperature Chamber Furnace", "Support high-temperature heat treatment, annealing, calcination, and sintering investigations.", "https://www.carbolite.com/products/chamber-furnaces/laboratory-furnaces/htf-high-temperature-chamber-furnaces/", "available", ("DMP",)),
    ("DECHANG GH4230 Metal Band Saw", "Prepare metal stock safely and efficiently before turning, milling, forming, or fabrication processes.", "https://www.alibaba.com/product-detail/DECHANG-GH4230-High-Efficiency-Mini-Metal_1601387433469.html", "new", ("DMP",)),
    ("InssTek MX-Lab Six-Nozzle Metal Additive Manufacturing System", "Build, repair, and investigate metal components through directed-energy-deposition additive manufacturing.", "https://www.insstek.com/products/mx-lab?ckattempt=3", "new", ("DMP",)),
    ("SYIL L3 CNC Lathe", "Support precision CNC turning, toolpath development, setup, production, and manufacturing instruction.", "https://syil.com/L3", "new", ("DMP",)),
    ("SYIL X9 5-Axis Vertical Machining Center", "Enable advanced multi-axis milling, complex-part production, and high-level CAD/CAM learning.", "https://syil.com/x9", "new", ("DMP",)),
    ("500-Ton Servo CNC Hydraulic Press", "Compact metal powder and support forming research before downstream sintering and material evaluation.", "https://www.yihui-press.com/dongguan-yihui-hydraulic-press-machine-for-metal-deep-drawing.html", "new", ("DMP",)),
    ("Metal Powder Water Atomization System", "Produce metal powder feedstock through controlled water atomization for materials and manufacturing research.", "https://en.hncpie.com/products_detail/17.html", "new", ("DMP",)),
    ("Anycubic FDM 3D Printing System with ACE Pro", "Support rapid prototyping and multicolor filament workflows with a compatible Anycubic FDM printer.", "https://store.anycubic.com/products/anycubic-ace-pro", "available", ("DMP",)),
    ("Automated Cooling and Spraying System", "Investigate cooling performance, spraying control, sensors, actuation, and energy-efficient operation.", "", "available", ("TES",)),
    ("Solar Tracking System", "Study solar positioning, tracking control, energy capture, measurement, and renewable-system performance.", "", "available", ("TES",)),
    ("Wind Turbine System", "Extend future learning and research in wind-energy conversion, measurement, control, and system performance.", "", "planned", ("TES",)),
    ("Robot with Artificial Vision System", "Combine robotics, machine vision, sensing, and control for Industry 4.0 learning activities.", "", "available", ("MAS",)),
    ("Four-Station Automation Simulation System", "Practice integrated sequencing, sensing, handling, control, and troubleshooting across four automated stations.", "", "available", ("MAS",)),
    ("Robot with Warehouse Automation System", "Explore robotic material handling, storage, retrieval, coordination, and warehouse automation.", "", "available", ("MAS",)),
    ("Industrial Electronic Circuit System", "Build and diagnose industrial electronic circuits used in machines, automation, and control systems.", "", "available", ("MAS",)),
    ("PLC Panel with Simulation System", "Program, simulate, commission, and troubleshoot PLC-based industrial control sequences.", "", "available", ("MAS",)),
    ("Universal Testing Machine", "Measure mechanical properties and material strength through controlled tensile, compression, and related tests.", "https://www.insize.com/testingmachines/UTM-GB.html", "available", ("ECM",)),
    ("Handheld LIBS Spectrometer", "Identify and evaluate material composition through rapid laser-induced breakdown spectroscopy.", "https://m.insize.com/page-35-2542.html", "available", ("ECM",)),
    ("Precision Metrology Equipment Package", "Verify dimensions, tolerances, inspection results, quality requirements, and engineering compliance.", "https://insizeus.com/tool.html", "available", ("ECM",)),
]


class Command(BaseCommand):
    help = "Seed the ME website with the approved initial program content and images."

    def add_arguments(self, parser):
        parser.add_argument(
            "--assets-dir",
            type=Path,
            default=settings.BASE_DIR.parent.parent / "assets",
            help="Path to the prepared website assets directory.",
        )

    def handle(self, *args, **options):
        assets_dir = options["assets_dir"].resolve()
        if not assets_dir.exists():
            self.stderr.write(self.style.ERROR(f"Assets directory not found: {assets_dir}"))
            return

        site = Site.objects.filter(is_default_site=True).first() or Site.objects.first()
        if not site:
            self.stderr.write(self.style.ERROR("No Wagtail site exists. Run migrations first."))
            return

        image_cache = {}

        def import_image(relative_path, title):
            if not relative_path:
                return None
            source = assets_dir / relative_path
            if not source.exists():
                self.stderr.write(self.style.WARNING(f"Missing image: {source}"))
                return None
            cache_key = str(source).lower()
            if cache_key in image_cache:
                return image_cache[cache_key]
            Image = get_image_model()
            existing = Image.objects.filter(title=title).first()
            if existing:
                image_cache[cache_key] = existing
                return existing
            with source.open("rb") as source_file:
                image = Image(title=title)
                image.file.save(source.name, File(source_file), save=True)
            image_cache[cache_key] = image
            return image

        hero_image = import_image("hero-lab.png", "ME RUPP robotics laboratory")
        settings_object, _ = ProgramSettings.objects.get_or_create(site=site)
        settings_object.hero_image = hero_image
        settings_object.facebook_url = (
            "https://www.facebook.com/profile.php?id=61589041923041"
        )
        settings_object.telegram_url = "https://t.me/mechanical_rupp"
        settings_object.save()

        for index, (title, description, image_path, media_kind) in enumerate(
            WHY_ITEMS, start=1
        ):
            WhyChooseItem.objects.update_or_create(
                title=title,
                defaults={
                    "sort_order": index,
                    "description": description,
                    "media_kind": media_kind,
                    "image": import_image(image_path, f"Why ME {index}: {title}"),
                },
            )

        focus_objects = {}
        facility_headings = {
            "DMP": "Design & Manufacturing Lab",
            "TES": "Thermofluid & Energy Systems Lab",
            "MAS": "Mechatronics & Automation Lab",
            "ECM": "Engineering Compliance & Management Lab",
        }
        for index, (code, title, description, accent, image_path) in enumerate(
            FOCUS_AREAS, start=1
        ):
            focus, _ = FocusArea.objects.update_or_create(
                code=code,
                defaults={
                    "sort_order": index,
                    "title": title,
                    "slug": slugify(title),
                    "description": description,
                    "accent_color": accent,
                    "image": import_image(image_path, f"{code}: {title}"),
                    "facility_heading": facility_headings[code],
                },
            )
            focus_objects[code] = focus

        course_objects = {}
        for year, theme, credits, description, courses in CURRICULUM:
            curriculum_year, _ = CurriculumYear.objects.update_or_create(
                year=year,
                defaults={
                    "sort_order": year,
                    "theme": theme,
                    "credit_count": credits,
                    "description": description,
                },
            )
            for index, (code, title, course_credits) in enumerate(courses, start=1):
                course, _ = Course.objects.update_or_create(
                    curriculum_year=curriculum_year,
                    code=code,
                    defaults={
                        "sort_order": index,
                        "title": title,
                        "credits": course_credits,
                        "semester": "1" if index <= 4 else "2",
                    },
                )
                course_objects[code] = course

        for focus_code, course_codes in FOCUS_COURSE_CODES.items():
            for course_code in course_codes:
                course = course_objects.get(course_code)
                if course:
                    course.focus_areas.add(focus_objects[focus_code])

        for index, (title, focus_codes, summary) in enumerate(RESEARCH, start=1):
            primary_focus = focus_objects[focus_codes[0]]
            project, _ = ResearchProject.objects.update_or_create(
                slug=slugify(title),
                defaults={
                    "sort_order": index,
                    "title": title,
                    "summary": summary,
                    "image": primary_focus.image,
                    "is_published": True,
                },
            )
            project.focus_areas.set(
                [focus_objects[focus_code] for focus_code in focus_codes]
            )

        for index, (name, partner_type, image_path) in enumerate(PARTNERS, start=1):
            Partner.objects.update_or_create(
                name=name,
                defaults={
                    "sort_order": index,
                    "partner_type": partner_type,
                    "logo": import_image(image_path, f"{name} logo"),
                },
            )

        for index, (
            name,
            description,
            reference_url,
            availability_status,
            focus_codes,
        ) in enumerate(FOCUS_EQUIPMENT, start=1):
            facility, _ = Facility.objects.update_or_create(
                name=name,
                defaults={
                    "sort_order": index,
                    "description": description,
                    "reference_url": reference_url,
                    "availability_status": availability_status,
                    "is_featured": False,
                },
            )
            facility.focus_areas.set(
                [focus_objects[focus_code] for focus_code in focus_codes]
            )

        for focus_code, detail_groups in FOCUS_DETAIL_ITEMS.items():
            focus = focus_objects[focus_code]
            for item_type, items in detail_groups.items():
                for index, (title, description) in enumerate(items, start=1):
                    FocusAreaDetailItem.objects.update_or_create(
                        focus_area=focus,
                        item_type=item_type,
                        title=title,
                        defaults={
                            "sort_order": index,
                            "description": description,
                        },
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Seeded program settings, 9 reasons, 4 focus areas, curriculum, "
                "research, focus details, partners, facilities, and media."
            )
        )
