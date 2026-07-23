from django.db import models
from django.utils import timezone
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet


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

    panels = [
        FieldPanel("sort_order"),
        FieldPanel("code"),
        FieldPanel("title"),
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("accent_color"),
        FieldPanel("image"),
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
    focus_area = models.ForeignKey(
        FocusArea,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="research_projects",
    )
    summary = models.TextField()
    body = RichTextField(blank=True)
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
        FieldPanel("focus_area"),
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
class FacultyMember(OrderedModel):
    name = models.CharField(max_length=160)
    role = models.CharField(max_length=160)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
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
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("bio"),
        FieldPanel("email"),
        FieldPanel("photo"),
        FieldPanel("focus_areas"),
        FieldPanel("is_published"),
    ]

    def __str__(self):
        return self.name


@register_snippet
class NewsEvent(OrderedModel):
    CONTENT_TYPES = (("news", "News"), ("event", "Event"))

    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default="news")
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    excerpt = models.TextField()
    body = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    event_date = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    panels = [
        FieldPanel("sort_order"),
        FieldPanel("content_type"),
        FieldPanel("title"),
        FieldPanel("slug"),
        FieldPanel("excerpt"),
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("event_date"),
        FieldPanel("published_at"),
        FieldPanel("is_published"),
    ]

    def __str__(self):
        return self.title


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
