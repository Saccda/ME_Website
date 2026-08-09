from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    MultipleChooserPanel,
)
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet

from .blocks import NewsBodyBlock, ResearchBodyBlock


class OrderedModel(models.Model):
    sort_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ("sort_order", "pk")


@register_setting
class ProgramSettings(BaseSiteSetting):
    program_name = models.CharField(max_length=120, default="Mechanical Engineering")
    program_short_name = models.CharField(max_length=20, default="ME")
    established_year = models.PositiveSmallIntegerField(default=2015)
    hero_title = models.CharField(max_length=160, default="Engineer Tomorrow,")
    hero_emphasis = models.CharField(max_length=160, default="Serve Cambodia.")
    hero_description = models.TextField(
        default=(
            "Build the machines, energy systems, and intelligent technologies "
            "that move our nation forward."
        )
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    what_is_me_eyebrow = models.CharField(
        max_length=120,
        default="What is mechanical engineering?",
    )
    what_is_me_heading = models.CharField(
        max_length=220,
        default="Designed by engineers. Built for the world.",
    )
    what_is_me_intro = models.TextField(
        default=(
            "From drones and vehicles to satellites, robots, and the cooling "
            "systems behind AI, mechanical engineers shape how modern products "
            "move, work, and endure."
        )
    )
    focus_section_eyebrow = models.CharField(
        max_length=120,
        default="Areas of focus",
    )
    focus_section_heading = models.CharField(
        max_length=220,
        default="Four paths. One purpose.",
    )
    focus_section_intro = models.TextField(
        default=(
            "Move fluently between theory, simulation, fabrication, testing, "
            "and responsible engineering practice."
        )
    )
    why_section_eyebrow = models.CharField(
        max_length=120,
        default="Why choose ME at RUPP?",
    )
    why_section_heading = models.CharField(
        max_length=220,
        default="Nine reasons. One future-ready program.",
    )
    why_section_intro = models.TextField(
        default=(
            "Our learning model brings technology, social responsibility, and "
            "active practice together so graduates leave ready to contribute "
            "from day one."
        )
    )
    partners_section_eyebrow = models.CharField(
        max_length=120,
        default="Partnership",
    )
    partners_section_heading = models.CharField(
        max_length=220,
        default="Education and industry, connected.",
    )
    partners_section_intro = models.TextField(
        default=(
            "Our partnerships connect learning with research, industry "
            "experience, and job opportunities for ME students."
        )
    )
    news_section_eyebrow = models.CharField(
        max_length=120,
        default="Latest news & activities",
    )
    news_section_heading = models.CharField(
        max_length=220,
        default="Mechanical Engineering in action",
    )
    news_section_intro = models.TextField(
        default=(
            "Explore our latest projects, learning experiences, partnerships, "
            "and contributions to industry and the community."
        )
    )
    news_section_cta_label = models.CharField(
        max_length=60,
        default="View all stories",
    )
    research_hero_eyebrow = models.CharField(
        max_length=120,
        default="Research at ME RUPP",
    )
    research_hero_title = models.CharField(
        max_length=220,
        default="Engineering research at the interface of ideas",
    )
    research_hero_description = models.TextField(
        default=(
            "Our work connects design, energy, automation, and responsible "
            "engineering to practical challenges in Cambodia and beyond."
        )
    )
    research_quote = models.TextField(
        default=(
            "Mechanical engineering research is strongest where disciplines "
            "meet and useful solutions begin to take shape."
        )
    )
    research_quote_attribution = models.CharField(
        max_length=220,
        default="Design · Energy · Automation · Responsible engineering",
    )
    research_areas_eyebrow = models.CharField(
        max_length=120,
        default="Explore research",
    )
    research_areas_heading = models.CharField(
        max_length=220,
        default="Investigate our four research areas",
    )
    research_areas_intro = models.TextField(
        default=(
            "Each area organizes expertise without limiting collaboration "
            "across disciplines."
        )
    )
    research_projects_eyebrow = models.CharField(
        max_length=120,
        default="Current research",
    )
    research_projects_heading = models.CharField(
        max_length=220,
        default="Explore current research projects",
    )
    research_projects_intro = models.TextField(
        default=(
            "Open a project through its primary area to see its full context "
            "and connected disciplines."
        )
    )
    research_collaboration_eyebrow = models.CharField(
        max_length=120,
        default="Research collaboration",
    )
    research_collaboration_heading = models.CharField(
        max_length=220,
        default="Good research grows through shared expertise.",
    )
    research_area_projects_eyebrow = models.CharField(
        max_length=120,
        default="Current investigations",
    )
    research_area_projects_intro = models.TextField(
        default=(
            "Projects may also appear in another research area when the work "
            "depends on shared expertise."
        )
    )
    research_boundaries_eyebrow = models.CharField(
        max_length=120,
        default="Connected by the problem",
    )
    research_boundaries_heading = models.CharField(
        max_length=220,
        default="Research areas guide collaboration. They do not limit it.",
    )
    vision = models.TextField(
        default=(
            "To become a leader in Mechanical Engineering Education by infusing "
            "technology and social engagement into teaching and learning, research, "
            "and innovation for the advancement of society"
        )
    )
    mission_one = models.TextField(
        default=(
            "To provide a modern mechanical engineering education by infusing social "
            "engagement and technology into educational activity for an effective "
            "educational program."
        )
    )
    mission_two = models.TextField(
        default=(
            "To collaborate with university partners on mechanical engineering to "
            "enforce proactive research activities that lead to an advancement of "
            "research and innovation."
        )
    )
    program_years = models.PositiveSmallIntegerField(default=4)
    credit_hours = models.PositiveSmallIntegerField(default=140)
    address = models.TextField(
        default=(
            "Faculty of Engineering, Royal University of Phnom Penh, "
            "Russian Federation Boulevard (110), Phnom Penh, Cambodia"
        )
    )
    email = models.EmailField(default="me.fe.rupp@gmail.com")
    phone = models.CharField(max_length=40, default="+855 78 727 085")
    facebook_url = models.URLField(blank=True)
    telegram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    application_url = models.URLField(blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("program_name"),
                FieldPanel("program_short_name"),
                FieldPanel("established_year"),
            ],
            heading="Program identity",
        ),
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_emphasis"),
                FieldPanel("hero_description"),
                FieldPanel("hero_image"),
            ],
            heading="Homepage hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel("what_is_me_eyebrow"),
                FieldPanel("what_is_me_heading"),
                FieldPanel("what_is_me_intro"),
            ],
            heading="Homepage: What is mechanical engineering?",
        ),
        MultiFieldPanel(
            [
                FieldPanel("focus_section_eyebrow"),
                FieldPanel("focus_section_heading"),
                FieldPanel("focus_section_intro"),
            ],
            heading="Homepage: Areas of focus",
        ),
        MultiFieldPanel(
            [
                FieldPanel("why_section_eyebrow"),
                FieldPanel("why_section_heading"),
                FieldPanel("why_section_intro"),
            ],
            heading="Homepage: Why choose ME?",
        ),
        MultiFieldPanel(
            [
                FieldPanel("partners_section_eyebrow"),
                FieldPanel("partners_section_heading"),
                FieldPanel("partners_section_intro"),
            ],
            heading="Homepage: Partnership",
        ),
        MultiFieldPanel(
            [
                FieldPanel("news_section_eyebrow"),
                FieldPanel("news_section_heading"),
                FieldPanel("news_section_intro"),
                FieldPanel("news_section_cta_label"),
            ],
            heading="Homepage: News & activities",
        ),
        MultiFieldPanel(
            [
                FieldPanel("research_hero_eyebrow"),
                FieldPanel("research_hero_title"),
                FieldPanel("research_hero_description"),
                FieldPanel("research_quote"),
                FieldPanel("research_quote_attribution"),
                FieldPanel("research_areas_eyebrow"),
                FieldPanel("research_areas_heading"),
                FieldPanel("research_areas_intro"),
                FieldPanel("research_projects_eyebrow"),
                FieldPanel("research_projects_heading"),
                FieldPanel("research_projects_intro"),
                FieldPanel("research_collaboration_eyebrow"),
                FieldPanel("research_collaboration_heading"),
            ],
            heading="Research landing page",
        ),
        MultiFieldPanel(
            [
                FieldPanel("research_area_projects_eyebrow"),
                FieldPanel("research_area_projects_intro"),
                FieldPanel("research_boundaries_eyebrow"),
                FieldPanel("research_boundaries_heading"),
            ],
            heading="Research area pages (shared copy)",
        ),
        MultiFieldPanel(
            [
                FieldPanel("vision"),
                FieldPanel("mission_one"),
                FieldPanel("mission_two"),
            ],
            heading="Vision and mission",
        ),
        MultiFieldPanel(
            [
                FieldPanel("program_years"),
                FieldPanel("credit_hours"),
                FieldPanel("address"),
                FieldPanel("email"),
                FieldPanel("phone"),
                FieldPanel("facebook_url"),
                FieldPanel("telegram_url"),
                FieldPanel("youtube_url"),
                FieldPanel("linkedin_url"),
                FieldPanel("application_url"),
            ],
            heading="Program information",
        ),
    ]


@register_snippet
class WhyChooseItem(OrderedModel):
    title = models.CharField(max_length=180)
    description = models.TextField()
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    media_kind = models.CharField(
        max_length=10,
        choices=(("photo", "Photo"), ("logo", "Logo")),
        default="photo",
    )

    panels = [
        FieldPanel("sort_order"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("image"),
        FieldPanel("media_kind"),
    ]

    class Meta(OrderedModel.Meta):
        verbose_name = "Why choose ME item"

    def __str__(self):
        return self.title


@register_snippet
class FocusArea(OrderedModel):
    code = models.CharField(max_length=8, unique=True)
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField()
    accent_color = models.CharField(max_length=12, default="#061b2b")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    overview_heading = models.CharField(
        max_length=220,
        default="Knowledge that becomes engineering ability.",
    )
    overview_intro = models.TextField(
        default=(
            "Connect classroom fundamentals with practical investigation, "
            "modern tools, teamwork, and evidence-based engineering decisions."
        )
    )
    facility_heading = models.CharField(
        max_length=220,
        default="Equipment and facilities",
    )
    facility_intro = models.TextField(
        default=(
            "Learning, research, prototyping, testing, and engineering services."
        )
    )
    curriculum_heading = models.CharField(
        max_length=220,
        default="A progressive four-year study path.",
    )
    curriculum_intro = models.TextField(
        default=(
            "Foundation subjects lead to specialist work, integrated projects, "
            "industry experience, and the final capstone."
        )
    )
    learning_heading = models.CharField(
        max_length=220,
        default="Active learning beyond memorization.",
    )
    learning_intro = models.TextField(
        default=(
            "Activities combine technical knowledge with communication, "
            "iteration, safety, and reflection."
        )
    )
    careers_heading = models.CharField(
        max_length=220,
        default="Where this focus can take you.",
    )
    careers_intro = models.TextField(
        default=(
            "Graduates can move across technical and leadership roles as their "
            "experience grows."
        )
    )
    research_heading = models.CharField(
        max_length=220,
        default="Research connected to this focus.",
    )
    research_intro = models.TextField(
        default=(
            "Explore current projects in Research & Innovation for full project "
            "details and related focus areas."
        )
    )
    research_question = models.TextField(
        blank=True,
        help_text="The guiding research question shown on this area's research page.",
    )
    research_overview = models.TextField(
        blank=True,
        help_text="Introduces what this area investigates on its research page.",
    )

    panels = [
        FieldPanel("sort_order"),
        FieldPanel("code"),
        FieldPanel("title"),
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("accent_color"),
        FieldPanel("image"),
        MultiFieldPanel(
            [
                FieldPanel("overview_heading"),
                FieldPanel("overview_intro"),
                FieldPanel("facility_heading"),
                FieldPanel("facility_intro"),
                FieldPanel("curriculum_heading"),
                FieldPanel("curriculum_intro"),
                FieldPanel("learning_heading"),
                FieldPanel("learning_intro"),
                FieldPanel("careers_heading"),
                FieldPanel("careers_intro"),
                FieldPanel("research_heading"),
                FieldPanel("research_intro"),
            ],
            heading="Focus page section copy",
        ),
        MultiFieldPanel(
            [
                FieldPanel("research_question"),
                FieldPanel("research_overview"),
            ],
            heading="Research area page",
        ),
    ]

    def __str__(self):
        return f"{self.code} — {self.title}"


@register_snippet
class CurriculumYear(OrderedModel):
    year = models.PositiveSmallIntegerField(unique=True)
    theme = models.CharField(max_length=160)
    credit_count = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True)

    panels = [
        FieldPanel("sort_order"),
        FieldPanel("year"),
        FieldPanel("theme"),
        FieldPanel("credit_count"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return f"Year {self.year}: {self.theme}"


@register_snippet
class Course(OrderedModel):
    SEMESTER_CHOICES = (("1", "Semester 1"), ("2", "Semester 2"), ("full", "Full year"))

    curriculum_year = models.ForeignKey(
        CurriculumYear, on_delete=models.CASCADE, related_name="courses"
    )
    code = models.CharField(max_length=30)
    title = models.CharField(max_length=180)
    credits = models.PositiveSmallIntegerField(default=3)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default="1")
    focus_areas = models.ManyToManyField(
        FocusArea,
        blank=True,
        related_name="courses",
        help_text="Focus areas that this course directly supports.",
    )

    panels = [
        FieldPanel("sort_order"),
        FieldPanel("curriculum_year"),
        FieldPanel("code"),
        FieldPanel("title"),
        FieldPanel("credits"),
        FieldPanel("semester"),
        FieldPanel("focus_areas"),
    ]

    class Meta(OrderedModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("curriculum_year", "code"), name="unique_course_code_per_year"
            )
        ]

    def __str__(self):
        return f"{self.code} — {self.title}"


@register_snippet
class ResearchProject(OrderedModel):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    focus_areas = models.ManyToManyField(
        FocusArea,
        blank=True,
        related_name="research_projects",
        help_text="Select every focus area connected to this project.",
    )
    summary = models.TextField()
    body = StreamField(
        ResearchBodyBlock(),
        blank=True,
        help_text=(
            "The project write-up. Add blocks, and drag them by the handle at "
            "the top right of each block to rearrange."
        ),
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)

    panels = [
        FieldPanel("sort_order"),
        FieldPanel("title"),
        FieldPanel("slug"),
        FieldPanel("focus_areas"),
        FieldPanel("summary"),
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("is_published"),
        FieldPanel("published_at"),
    ]

    def __str__(self):
        return self.title


@register_snippet
class Partner(OrderedModel):
    PARTNER_TYPES = (
        ("industry", "Industry"),
        ("academic", "Academic"),
        ("government", "Government"),
        ("institutional", "Institutional"),
    )

    name = models.CharField(max_length=180)
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPES)
    website = models.URLField(blank=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("sort_order"),
        FieldPanel("name"),
        FieldPanel("partner_type"),
        FieldPanel("website"),
        FieldPanel("logo"),
    ]

    def __str__(self):
        return self.name


@register_snippet
class Opportunity(OrderedModel):
    OPPORTUNITY_TYPES = (
        ("job", "Job"),
        ("internship", "Internship"),
        ("scholarship", "Scholarship"),
        ("training", "Training"),
    )

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    opportunity_type = models.CharField(
        max_length=20,
        choices=OPPORTUNITY_TYPES,
        default="job",
    )
    partner = models.ForeignKey(
        Partner,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="opportunities",
    )
    announcement_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=(
            "Upload the partner's hiring poster or announcement artwork. "
            "A landscape 3:2 image is recommended."
        ),
    )
    focus_areas = models.ManyToManyField(
        FocusArea,
        blank=True,
        related_name="opportunities",
        help_text="Focus areas most relevant to this opportunity.",
    )
    summary = models.TextField()
    body = RichTextField(blank=True)
    location = models.CharField(max_length=180, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    application_url = models.URLField(blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(
        default=False,
        help_text="Prioritize this announcement on the homepage.",
    )

    panels = [
        FieldPanel("sort_order"),
        FieldPanel("title"),
        FieldPanel("slug"),
        FieldPanel("opportunity_type"),
        FieldPanel("partner"),
        FieldPanel("announcement_image"),
        FieldPanel("focus_areas"),
        FieldPanel("summary"),
        FieldPanel("body"),
        FieldPanel("location"),
        FieldPanel("application_deadline"),
        FieldPanel("application_url"),
        FieldPanel("published_at"),
        FieldPanel("is_published"),
        FieldPanel("is_featured"),
    ]

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Opportunities"

    def __str__(self):
        return self.title


@register_snippet
class Facility(OrderedModel):
    AVAILABILITY_CHOICES = (
        ("available", "Available"),
        ("new", "New equipment"),
        ("commissioning", "Commissioning"),
        ("planned", "Planned"),
    )

    name = models.CharField(max_length=180)
    description = models.TextField()
    reference_url = models.URLField(
        blank=True,
        help_text="Manufacturer or technical reference page for this machine.",
    )
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default="available",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show this equipment item in the homepage learning environment section.",
    )
    focus_areas = models.ManyToManyField(
        FocusArea,
        blank=True,
        related_name="facilities",
        help_text="Focus areas that use this equipment or facility.",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("sort_order"),
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("reference_url"),
        FieldPanel("availability_status"),
        FieldPanel("image"),
        FieldPanel("is_featured"),
        FieldPanel("focus_areas"),
    ]

    def __str__(self):
        return self.name


@register_snippet
class FocusAreaDetailItem(OrderedModel):
    ITEM_TYPES = (
        ("outcome", "Learning outcome"),
        ("activity", "Learning activity"),
        ("career", "Career pathway"),
        ("theme", "Research theme"),
    )

    focus_area = models.ForeignKey(
        FocusArea,
        on_delete=models.CASCADE,
        related_name="detail_items",
    )
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)

    panels = [
        FieldPanel("sort_order"),
        FieldPanel("focus_area"),
        FieldPanel("item_type"),
        FieldPanel("title"),
        FieldPanel("description"),
    ]

    class Meta(OrderedModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("focus_area", "item_type", "title"),
                name="unique_focus_detail_item",
            )
        ]
        verbose_name = "Focus area detail"

    def __str__(self):
        return f"{self.focus_area.code} — {self.title}"


@register_snippet
class FacultyMember(ClusterableModel, OrderedModel):
    LIST_HELP = "One entry per line."

    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, blank=True)
    credentials = models.CharField(
        max_length=80,
        blank=True,
        help_text="Post-nominal qualification, for example Ph.D. or M.Eng.",
    )
    role = models.CharField(max_length=160)
    statement = models.TextField(
        blank=True,
        help_text=(
            "One sentence shown as the large heading on the profile page, "
            "for example: Sophy Soun connects engineering theory with "
            "experimentation and practical laboratory learning. "
            "Left blank, the first sentence of the biography is used."
        ),
    )
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    office = models.CharField(
        max_length=120,
        blank=True,
        help_text="Room or building, for example Engineering Building, Room 204.",
    )
    research_interests = models.TextField(blank=True, help_text=LIST_HELP)
    education = models.TextField(
        blank=True,
        help_text="One qualification per line, for example: Ph.D. Mechanical Engineering, University, 2018",
    )
    courses_taught = models.TextField(blank=True, help_text=LIST_HELP)
    publications = models.TextField(blank=True, help_text=LIST_HELP)
    profile_url = models.URLField(
        blank=True,
        help_text="Optional external profile, for example Google Scholar or ORCID.",
    )
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    focus_areas = models.ManyToManyField(FocusArea, blank=True, related_name="faculty")
    is_published = models.BooleanField(default=True)

    panels = [
        FieldPanel("sort_order"),
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("slug"),
                FieldPanel("credentials"),
                FieldPanel("role"),
                FieldPanel("photo"),
                FieldPanel("focus_areas"),
            ],
            heading="Identity",
        ),
        MultiFieldPanel(
            [
                FieldPanel("office"),
                FieldPanel("email"),
                FieldPanel("phone"),
                FieldPanel("profile_url"),
            ],
            heading="Contact",
        ),
        MultiFieldPanel(
            [
                FieldPanel("statement"),
                FieldPanel("bio"),
                FieldPanel("research_interests"),
                FieldPanel("education"),
                FieldPanel("courses_taught"),
                FieldPanel("publications"),
            ],
            heading="Profile",
        ),
        InlinePanel(
            "work_items",
            heading="Selected work",
            label="Card",
            help_text=(
                "Cards shown in the Selected work row on this member's profile "
                "page. Leave empty to build the row automatically from the "
                "research projects, research themes, and teaching of the focus "
                "areas above."
            ),
        ),
        FieldPanel("is_published"),
    ]

    # ClusterableModel comes first in the bases, so its empty Meta would
    # otherwise win and the directory would lose its sort order.
    class Meta(OrderedModel.Meta):
        pass

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:180]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class FacultyWorkItem(Orderable):
    """One card in the Selected work row of a faculty profile page.

    A member's work is not only research, so the badge is free text rather than
    a fixed list: an author can label a card Research project, Mentorship,
    Industry collaboration, or anything else that describes it honestly.
    """

    member = ParentalKey(
        FacultyMember,
        on_delete=models.CASCADE,
        related_name="work_items",
    )
    badge = models.CharField(
        max_length=40,
        default="Research project",
        help_text="Label on the gold tab, for example Teaching & research.",
    )
    title = models.CharField(max_length=180)
    summary = models.TextField(blank=True)
    meta = models.CharField(
        max_length=120,
        blank=True,
        help_text="Small underlined line above the title, for example "
        "Automation · Environmental control.",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    link_url = models.CharField(
        max_length=300,
        blank=True,
        help_text="Where the card goes. A path on this site such as "
        "/research/projects/metal-recycling, or a full external address.",
    )
    link_label = models.CharField(
        max_length=60,
        blank=True,
        default="Explore the work",
        help_text="Text of the link at the foot of the card.",
    )

    panels = [
        FieldPanel("badge"),
        FieldPanel("title"),
        FieldPanel("meta"),
        FieldPanel("summary"),
        FieldPanel("image"),
        FieldPanel("link_url"),
        FieldPanel("link_label"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Faculty work card"

    def __str__(self):
        return f"{self.member.name} — {self.title}"


@register_snippet
class NewsEvent(ClusterableModel, OrderedModel):
    CONTENT_TYPES = (("news", "News"), ("event", "Event"))

    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default="news")
    category = models.CharField(
        max_length=80,
        blank=True,
        help_text=(
            "Small gold label above the title, for example Projects & "
            "Community or International Engagement. Free text, so the section "
            "can carry more than news."
        ),
    )
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    author = models.CharField(
        max_length=160,
        blank=True,
        help_text=(
            "Byline shown under the headline, for example "
            "Sok Dara, Communications Officer."
        ),
    )
    excerpt = models.TextField()
    body = StreamField(
        NewsBodyBlock(),
        blank=True,
        help_text=(
            "The story itself. Add blocks, and drag them by the handle at the "
            "top right of each block to rearrange."
        ),
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    event_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Event start",
    )
    event_end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Event end",
        help_text=(
            "Only for an event running over more than one day. Leave empty for "
            "a single-day event. The event stays listed as upcoming until this "
            "date passes."
        ),
    )
    published_at = models.DateTimeField(default=timezone.now)
    announce = models.BooleanField(
        default=False,
        verbose_name="Show in the announcement card",
        help_text=(
            "Surfaces this entry in the small card at the corner of the "
            "homepage, for something a visitor should not have to scroll to "
            "find. An event stops showing once its date has passed."
        ),
    )
    announcement_cta = models.CharField(
        max_length=40,
        blank=True,
        help_text="Button on the announcement card. Defaults to Event details.",
    )
    is_published = models.BooleanField(default=True)

    panels = [
        FieldPanel("sort_order"),
        FieldPanel("content_type"),
        FieldPanel("category"),
        FieldPanel("title"),
        FieldPanel("slug"),
        FieldPanel("author"),
        FieldPanel("excerpt"),
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("event_date"),
        FieldPanel("event_end_date"),
        FieldPanel("published_at"),
        MultiFieldPanel(
            [
                FieldPanel("announce"),
                FieldPanel("announcement_cta"),
            ],
            heading="Announcement card",
        ),
        # "Add multiple images" opens the chooser in multi-select mode, so a
        # whole set is picked -- or dragged in and uploaded -- in one pass
        # instead of one image at a time.
        MultipleChooserPanel(
            "gallery_images",
            chooser_field_name="image",
            heading="Story gallery",
            label="Image",
            help_text=(
                "Shown as a gallery at the end of the story. Use Add multiple "
                "images to pick or upload a whole set at once, then drag to "
                "reorder."
            ),
        ),
        FieldPanel("is_published"),
    ]

    # ClusterableModel comes first in the bases, so its empty Meta would
    # otherwise win and the listing would lose its sort order.
    class Meta(OrderedModel.Meta):
        pass

    def __str__(self):
        return self.title


class NewsEventGalleryImage(Orderable):
    """One picture in a story's gallery.

    A child model rather than a StreamField block, because only a model
    relation can use MultipleChooserPanel -- which is the only place in Wagtail
    where several images are chosen in a single action.
    """

    story = ParentalKey(
        NewsEvent,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
    )
    caption = models.CharField(max_length=250, blank=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Story gallery image"

    def __str__(self):
        return f"{self.story.title} - {self.image.title}"


class Inquiry(models.Model):
    INQUIRY_TYPES = (
        ("general", "General"),
        ("admission", "Admission"),
        ("collaboration", "Collaboration"),
    )
    STATUS_CHOICES = (
        ("new", "New"),
        ("in_progress", "In progress"),
        ("resolved", "Resolved"),
        ("spam", "Spam"),
    )

    inquiry_type = models.CharField(
        max_length=20, choices=INQUIRY_TYPES, default="general"
    )
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    organization = models.CharField(max_length=180, blank=True)
    subject = models.CharField(max_length=180)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name}: {self.subject}"
