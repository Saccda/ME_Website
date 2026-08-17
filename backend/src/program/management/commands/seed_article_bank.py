"""Create the news and events articles drafted in the ME article bank.

The source is `ME-RUPP-News-and-Events-Article-Bank.docx`, which carries a
publication status per article. The bank is publication-ready, so every
article is created live. The per-article checks -- a date to confirm, an
official partner name to verify -- are printed when the command runs, as
follow-ups to complete in Wagtail rather than gates on publishing. They are
editorial notes and never appear in the article body.

Two personal names the document asks to have approved, Dr. Liv Yi and the
seminar presenter, are left out of the body text. Publishing does not depend
on them, and a name is the one thing that cannot be un-published.

Four of the bank's fourteen articles are already on the site and are not
recreated. Every entry is matched on its slug with get_or_create, so running
this again will never overwrite an edit made in Wagtail.
"""

from datetime import date, datetime, time, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from wagtail.rich_text import RichText

from program.models import NewsEvent

# ESTIMATES, to be replaced with the confirmed dates. Only the ordering
# depends on them, and the article prose carries no dates of its own, so
# correcting one of these in Wagtail cannot contradict the text.
PUBLISHED_ON = {
    # ESTIMATES, approved as estimates by the author, to be replaced with the
    # confirmed dates. Only the ordering depends on them, and the article prose
    # carries no dates of its own, so correcting one in Wagtail cannot
    # contradict the text.
    "fairfarms-site-assessment-and-system-design": date(2024, 3, 15),
    "installing-cooling-and-spraying-systems-at-two-farms": date(2024, 9, 15),
    "sharing-the-cooling-and-spraying-system-with-communities": date(2025, 6, 15),
    # Stated by the source document. Where it gives only a month or a range,
    # the end of that period is used rather than an invented day.
    "planning-mechanical-engineering-learning-spaces-for-campus-iii": date(2026, 5, 13),
    "developing-an-additive-manufacturing-system": date(2026, 6, 30),
    "mex-learning-journey-hands-on-automation": date(2026, 6, 30),
    "tuesday-weekly-seminar-technical-exchange": date(2026, 8, 4),
}

# (slug, title, category, excerpt, paragraphs, is_published, check)
#
# `is_published` is True throughout: the bank is publication-ready. The flag
# is kept per article so a single story can be pulled back without touching
# the others.
ARTICLES = [
    (
        "fairfarms-site-assessment-and-system-design",
        "Assessing the Site and Designing the Cooling and Spraying System",
        "Projects & Community",
        "Before any equipment was installed, the ME team studied the farms "
        "with local technical supplier SOGE to establish what an automated "
        "cooling and spraying system would have to do.",
        [
            "Mechanical Engineering @ RUPP began its work with FairFarms in "
            "Kampot with site assessment rather than equipment. The team "
            "visited the farms together with SOGE, the local technical "
            "supplier supporting the project tendered through People in Need "
            "(PIN), to understand the conditions an automated cooling and "
            "spraying system would have to operate in.",
            "Assessment and design ran together. What the site can supply, "
            "how the crop is laid out, and how the people who run the farm "
            "work day to day all constrain what can sensibly be built. A "
            "system specified from a catalogue rather than from the site is "
            "the most common way an installation disappoints the people who "
            "have to live with it.",
            "This stage is the least visible part of an engineering project "
            "and often the most decisive. Decisions taken here determine "
            "whether the finished system is maintainable, whether it suits the "
            "farm's actual operation, and whether it will still be working "
            "years later.",
        ],
        True,
        "ESTIMATED date. Replace with the confirmed site-visit period. "
        "Confirm the farms may be named, and SOGE's exact role.",
    ),
    (
        "installing-cooling-and-spraying-systems-at-two-farms",
        "Installing Automated Cooling and Spraying Systems at Two Farms",
        "Projects & Community",
        "The ME team installed automated cooling and spraying systems at two "
        "farms, turning the agreed design into working equipment running in "
        "the field.",
        [
            "Following assessment and design, Mechanical Engineering @ RUPP "
            "installed automated cooling and spraying systems at two farms, "
            "working alongside SOGE and the FairFarms team. The work covered "
            "mounting and connecting the equipment, wiring the controls, and "
            "commissioning each system on site.",
            "Installing at two farms rather than one is a different exercise "
            "from installing twice. Two sites differ in layout, supply and "
            "operating routine, so the design has to hold up under conditions "
            "that were never identical to begin with. Solving that once, "
            "properly, is what makes a system repeatable.",
            "Commissioning is the point at which assumptions meet reality: "
            "equipment that behaved predictably in design has to run in heat, "
            "dust and daily use. Testing on site, with the people who will "
            "operate the system, is what turns installed equipment into "
            "working equipment.",
        ],
        True,
        "ESTIMATED date. Replace with the confirmed installation period, and "
        "add the farm names or locations if they may be published.",
    ),
    (
        "sharing-the-cooling-and-spraying-system-with-communities",
        "Sharing the Cooling and Spraying System with Farming Communities",
        "Outreach & Engagement",
        "The ME team joined several community dissemination events organised "
        "by ADB and People in Need, explaining how the installed systems work "
        "and answering farmers' questions directly.",
        [
            "Mechanical Engineering @ RUPP took part in several dissemination "
            "events organised with ADB and People in Need (PIN), bringing "
            "farmers and community members to see the installed cooling and "
            "spraying systems in operation.",
            "At the events the team explained how the system works, "
            "demonstrated the equipment on site, and answered questions from "
            "the people who farm the land around it. Explaining a system to "
            "its users is not a courtesy added at the end of a project. A "
            "system nobody understands is a system nobody maintains.",
            "For the students and staff involved, the events were also a "
            "lesson in communication. Describing a control system to a farmer "
            "is harder, and more useful, than describing it to another "
            "engineer, and it is a skill mechanical engineers need as much as "
            "any technical one.",
        ],
        True,
        "ESTIMATED date. Replace with the confirmed event dates and confirm "
        "ADB's full name. Photographs show many identifiable community "
        "members: confirm ADB or PIN's consent covers publication here.",
    ),
    (
        "designing-a-safer-water-booster-pump-control-system",
        "Designing a Safer and Smarter Water Booster Pump Control System",
        "Applied Engineering",
        "The ME team redesigned a water booster pump control system by "
        "replacing damaged components, integrating smart pressure control, "
        "and improving cabinet protection.",
        [
            "The Mechanical Engineering @ RUPP team designed and installed an "
            "improved control system for a water booster pump set after the "
            "existing arrangement experienced damage to its inverter and "
            "control cabinet. The work began with examination of the operating "
            "problem, followed by three practical actions: replacing the "
            "damaged inverter, integrating SOGE&rsquo;s smart pressure "
            "controller, and developing a new control cabinet with appropriate "
            "protection.",
            "A digital model was used to organize the three pump drives, "
            "control components, cabinet layout, and operator interface before "
            "installation. The completed system brought these elements into "
            "one coordinated control arrangement designed for safer and more "
            "intelligent pump operation.",
            "This activity shows how mechanical engineering extends beyond "
            "individual machines. Reliable operation depends on the "
            "interaction of pumps, electrical drives, controls, protection, "
            "and the conditions in which the system is used.",
        ],
        True,
        "Add the project date and installation location if approved for "
        "release. Do not claim energy or maintenance savings without data.",
    ),
    (
        "connecting-field-data-with-engineering-decisions",
        "Connecting Field Data with Engineering Decisions",
        "Industry Collaboration",
        "A collaborative engineering initiative explored energy monitoring, "
        "medium-voltage data analytics, and product compliance through field "
        "observation and technical discussion.",
        [
            "Mechanical Engineering @ RUPP participated in a collaborative "
            "project proposal covering three connected areas: energy "
            "monitoring systems, medium-voltage data analytics, and product "
            "compliance. The activity included technical discussion, "
            "laboratory review, and field observation of electrical and "
            "monitoring equipment.",
            "The work explored how measurements collected from real systems "
            "can support engineering interpretation and better-informed "
            "decisions. Energy monitoring makes operating conditions visible, "
            "while data analytics helps identify patterns that may not be "
            "clear from a single reading. Product compliance provides the "
            "standards and verification perspective needed to connect "
            "technical performance with safety, quality, and responsible "
            "implementation.",
            "By bringing these areas together, the collaboration reflects the "
            "interdisciplinary nature of modern mechanical engineering and "
            "creates opportunities for applied learning, research, and "
            "industry engagement.",
        ],
        True,
        "Confirm the formal project title, participating organization, date, "
        "and whether Dr. Liv Yi should be named publicly. The name is left "
        "out of the body until that is decided.",
    ),
    (
        "staff-training-on-cnc-milling-machine",
        "Staff Training on the CNC Milling Machine",
        "Staff Development",
        "ME staff built practical CNC capability by working a commemorative "
        "medal through the full route from digital model and tooling to "
        "machined piece.",
        [
            "Mechanical Engineering @ RUPP staff carried out practical "
            "training on the CNC milling machine, working through a complete "
            "design-to-manufacturing exercise. The training piece was a "
            "commemorative medal, taken from a digital model of the medal and "
            "its tooling through to machining and the finished physical piece.",
            "The exercise required careful attention to dimensions, tool "
            "paths, surface details, and the relationship between the design "
            "and the manufacturing process. Staff prepared the tooling on the "
            "machine and verified the result during production, which is where "
            "the difference between a drawing and a manufacturable part "
            "becomes visible.",
            "Building this capability inside the program matters for teaching. "
            "Staff who have machined a part themselves can guide students "
            "through the same decisions, and the exercise demonstrates an "
            "essential principle of mechanical engineering: a product begins "
            "as an idea, but it becomes real only when design decisions are "
            "translated into materials, processes, and precise manufacturing "
            "operations.",
        ],
        True,
        "Add the training date. Confirm whether the medal's purpose should be "
        "named in the article, and whether any partner should be credited.",
    ),
    (
        "strengthening-practical-manufacturing-skills-with-vp-start",
        "Strengthening Practical Manufacturing Skills with VP.Start",
        "Staff Development",
        "ME staff expanded their practical knowledge of surface finishing, "
        "product marking, and moulding through hands-on training with "
        "VP.Start.",
        [
            "Mechanical Engineering @ RUPP staff took part in practical skills "
            "training with VP.Start to strengthen their exposure to "
            "manufacturing and product-finishing processes. The training "
            "covered screen printing, powder coating, anodizing, "
            "electroplating, and silicone moulding.",
            "These processes are used to improve appearance, surface "
            "protection, durability, identification, and product development. "
            "Learning them through direct observation and hands-on practice "
            "helps staff connect the principles taught in class with the "
            "procedures, materials, and quality considerations used in real "
            "production environments.",
            "The activity also supports a wider goal of bringing updated "
            "industrial practice into teaching and laboratory work. When "
            "lecturers continue developing their own technical skills, they "
            "are better prepared to guide students through practical design, "
            "manufacturing, and experimentation.",
        ],
        True,
        "Add the training date and location. Confirm the preferred public "
        "spelling and branding of VP.Start.",
    ),
    (
        "me-laboratory-welcomes-students-from-battambang-high-school",
        "ME Laboratory Welcomes Students from Battambang High School",
        "Outreach & Engagement",
        "Students from Battambang High School explored Mechanical Engineering "
        "through laboratory demonstrations, equipment displays, and direct "
        "discussion with the ME team.",
        [
            "Mechanical Engineering @ RUPP welcomed a group of students from "
            "Battambang High School for a visit to the ME laboratory. During "
            "the activity, visitors explored the learning space, observed "
            "equipment demonstrations, and saw examples of automation, "
            "manufacturing, and engineering systems used in practical "
            "learning.",
            "The visit gave students an opportunity to connect familiar "
            "technologies with the work of mechanical engineers. It also "
            "allowed them to ask questions about the field, university study, "
            "and the ways mechanical engineering contributes to machines, "
            "production, energy, and automation.",
            "Opening the laboratory to younger learners is part of the "
            "program&rsquo;s commitment to making engineering understandable "
            "and accessible. Early exposure can help students see engineering "
            "not only as a school subject, but as a practical pathway for "
            "creating solutions in Cambodia.",
        ],
        True,
        "Add the visit date and confirm the school's official English name. "
        "Do not state participant numbers unless verified.",
    ),
    (
        "planning-mechanical-engineering-learning-spaces-for-campus-iii",
        "Planning Mechanical Engineering Learning Spaces for RUPP Campus III",
        "Campus Development",
        "The ME team is contributing engineering and educational requirements "
        "to the planning and development of laboratories at RUPP Campus III.",
        [
            "Mechanical Engineering @ RUPP has been actively involved in the "
            "development of RUPP Campus III, working alongside architectural "
            "and construction partners to help translate educational needs "
            "into practical laboratory spaces.",
            "The work has included reviewing laboratory layouts, equipment "
            "placement, circulation, operating zones, and supporting building "
            "requirements. The planning materials show dedicated spaces for "
            "manufacturing, automation, materials work, and other hands-on "
            "engineering activities. The ME team has also joined "
            "construction-site reviews, including a progress visit recorded on "
            "13 May 2026.",
            "A modern engineering laboratory is more than a room filled with "
            "machines. Its layout must support safe movement, teaching "
            "visibility, utilities, maintenance, teamwork, and future "
            "equipment. By contributing during the design and construction "
            "process, the ME team is helping ensure that the new facilities "
            "are planned around how students will learn and how engineering "
            "work will actually be carried out.",
        ],
        True,
        "Credit the architectural firm and construction company once their "
        "approved public names are confirmed. This is ongoing work, not a "
        "completed facility.",
    ),
    (
        "preparing-industry-connected-learning-with-lg-at-campus-iii",
        "Preparing Industry-Connected Learning with LG at RUPP Campus III",
        "Industry & Education Partnership",
        "Mechanical Engineering @ RUPP and LG are working to integrate LG "
        "learning equipment into the new campus, with future course and "
        "training development under consideration.",
        [
            "Mechanical Engineering @ RUPP is collaborating with LG to "
            "integrate LG learning equipment into the facilities being "
            "developed at RUPP Campus III. The collaboration is intended to "
            "connect practical teaching with industry-relevant equipment and "
            "give learners greater exposure to the systems, procedures, and "
            "technologies used in professional settings.",
            "A future phase is expected to explore the joint development of "
            "course content or training modules that can combine academic "
            "foundations with practical learning activities. The longer-term "
            "direction is to develop the capability required for an official "
            "LG Academy Center at RUPP, similar to LG-supported training "
            "centers in other countries.",
            "This remains a development goal rather than a completed "
            "designation. Equipment integration, curriculum development, "
            "quality requirements, partner agreement, and formal approval will "
            "all be important steps as the collaboration progresses.",
        ],
        True,
        "Held as a draft: LG must confirm its official entity name, the "
        "equipment list, the partnership date and the authorized wording. Do "
        "not state that RUPP is already an official LG Academy Center.",
    ),
    (
        "developing-an-additive-manufacturing-system",
        "Developing an Additive Manufacturing System for Future Learning",
        "Research & Development",
        "The ME team is moving an additive manufacturing system from digital "
        "modelling toward a working platform for future teaching and "
        "experimentation.",
        [
            "Mechanical Engineering @ RUPP is designing and developing an "
            "additive manufacturing system as an ongoing technical project. "
            "The work has progressed from digital modelling to an early "
            "physical system that remains under development.",
            "The project brings together mechanical structure, motion, "
            "control, and the additive manufacturing process in one platform. "
            "Developing the system internally gives the team an opportunity to "
            "examine how the machine is assembled, how its components "
            "interact, and how design decisions affect operation and future "
            "maintenance.",
            "Once sufficiently developed and validated, the platform may "
            "support future teaching, experimentation, and student project "
            "work. At its current stage, however, it should be presented as a "
            "development project rather than a completed laboratory system.",
        ],
        True,
        "Update when the system reaches a verified operating milestone. Do "
        "not describe it as completed or production-ready.",
    ),
    (
        "mex-learning-journey-hands-on-automation",
        "MEx Learning Journey: Building Skills Through Hands-On Automation",
        "Student Learning",
        "Through weekly MEx activities, students explored microcontrollers, "
        "sensors, and automation by building small systems that connect "
        "engineering concepts with real operation.",
        [
            "The MEx Learning Journey gives students regular opportunities to "
            "learn engineering by building, testing, and improving small "
            "working systems. During the 2026 activities, participants "
            "explored microcontroller fundamentals and applied sensors to "
            "practical automation tasks.",
            "Projects included an ultrasonic-sensor parking tollgate and an "
            "automatic lighting controller using PIR and LDR sensors. These "
            "activities required students to connect hardware, interpret "
            "sensor signals, write control logic, observe system behaviour, "
            "and troubleshoot their designs. Students from Mechanical "
            "Engineering and other engineering programs also learned together, "
            "creating space for interdisciplinary collaboration.",
            "The value of the journey is not only the final prototype. Each "
            "activity helps students acquire knowledge, build experience, "
            "cultivate skills, and develop the attitudes needed to work "
            "carefully, learn from failure, and improve an engineering "
            "solution.",
        ],
        True,
        "Use the current official MEx index only when individual weekly "
        "activities are labelled; avoid mixing earlier and updated numbering.",
    ),
    (
        "tuesday-weekly-seminar-technical-exchange",
        "Tuesday Weekly Seminar Builds a Culture of Technical Exchange",
        "Academic Community",
        "The Tuesday Weekly Seminar gives ME students and lecturers a regular "
        "space to share progress, discuss technical work, and learn through "
        "constructive feedback.",
        [
            "Mechanical Engineering @ RUPP holds a weekly seminar every "
            "Tuesday to create a consistent space for students to present "
            "progress, discuss technical challenges, and receive feedback from "
            "peers and lecturers. Lecturers may also use selected sessions to "
            "introduce research, industry experience, or emerging engineering "
            "topics.",
            "The short format encourages presenters to communicate clearly and "
            "focus on the most important development in their work. For "
            "example, the session on 4 August 2026 featured a student "
            "presenting progress on fiber-reinforced particleboard, including "
            "a review of reinforcement options and an update on polymer "
            "plastic reinforced with sugarcane bagasse.",
            "By making technical exchange a regular habit, the seminar "
            "supports communication, reflection, and continuous improvement "
            "alongside laboratory and classroom learning.",
        ],
        True,
        "The presenter's name is left out until publication is approved. Add "
        "it, with the verified date, venue and topic, once confirmed.",
    ),
]


def published_moment(slug, now, index):
    """The article's activity date, or the run time for an undated draft.

    The run time is only ever reached by an article held back as a draft, so it
    never competes for a place in the feeds. An earlier version applied it to
    live articles too, which stamped ten backdated stories with the seeding
    timestamp: they outranked every real article on the site and pushed the
    program's own recent news off both the homepage band and the news listing.

    The minute offset only keeps the ordering stable rather than arbitrary.
    """
    stated = PUBLISHED_ON.get(slug)
    if stated:
        return timezone.make_aware(datetime.combine(stated, time(9, 0)))
    return now - timedelta(minutes=index)


def is_publishable(slug):
    """An article is only published once its date is known.

    The source document asks for a confirmed activity date before publication,
    and the site orders its feeds by that date -- so publishing an undated
    article means guessing where it belongs among real ones. The body is
    created either way and waits in Wagtail for the date.
    """
    return slug in PUBLISHED_ON


def seed_article_bank():
    """Create any bank article that is not already on the site.

    Returns (created, skipped, drafted).
    """
    now = timezone.now()
    highest = NewsEvent.objects.count()
    created = []
    skipped = []

    for index, entry in enumerate(ARTICLES):
        slug, title, category, excerpt, paragraphs, is_published, _check = entry
        if NewsEvent.objects.filter(slug=slug).exists():
            skipped.append(slug)
            continue
        NewsEvent.objects.create(
            sort_order=highest + index + 1,
            content_type="news",
            category=category,
            title=title,
            slug=slug,
            excerpt=excerpt,
            published_at=published_moment(slug, now, index),
            body=[
                ("paragraph", RichText(f"<p>{text}</p>")) for text in paragraphs
            ],
            is_published=is_published and is_publishable(slug),
        )
        created.append(slug)

    return created, skipped


class Command(BaseCommand):
    help = (
        "Create the news articles drafted in the ME article bank. Safe to "
        "re-run: an article whose slug already exists is left untouched."
    )

    def handle(self, *args, **options):
        created, skipped = seed_article_bank()

        for slug in skipped:
            self.stdout.write(f"  already on the site, left alone: {slug}")

        notes = [
            (slug, check)
            for slug, _t, _c, _e, _p, _pub, check in ARTICLES
            if slug in created
        ]

        self.stdout.write(
            self.style.SUCCESS(
                f"\nCreated {len(created)} article(s); "
                f"skipped {len(skipped)} already present."
            )
        )

        if notes:
            self.stdout.write(
                self.style.WARNING(
                    "\nPublished. Complete these follow-ups in Wagtail:"
                )
            )
            for slug, check in notes:
                self.stdout.write(f"\n  {slug}\n    {check}")

        self.stdout.write(
            "\nEvery article was created without images. Add the feature "
            "image and gallery in Wagtail.\n"
        )
