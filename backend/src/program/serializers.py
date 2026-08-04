from rest_framework import serializers
from wagtail.rich_text import expand_db_html

from .models import (
    Course,
    CurriculumYear,
    Facility,
    FacultyMember,
    FacultyWorkItem,
    FocusArea,
    FocusAreaDetailItem,
    Inquiry,
    NewsEvent,
    Opportunity,
    Partner,
    ProgramSettings,
    ResearchProject,
    WhyChooseItem,
)


def image_url(image, request=None):
    if not image:
        return None
    url = image.file.url
    return request.build_absolute_uri(url) if request else url


class ImageSerializerMixin:
    def get_image(self, obj):
        request = self.context.get("request")
        image = getattr(obj, self.image_field, None)
        return image_url(image, request)


class WhyChooseItemSerializer(ImageSerializerMixin, serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_field = "image"

    class Meta:
        model = WhyChooseItem
        fields = ("id", "sort_order", "title", "description", "media_kind", "image")


class FocusAreaSerializer(ImageSerializerMixin, serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    career_paths = serializers.SerializerMethodField()
    research_themes = serializers.SerializerMethodField()
    image_field = "image"

    def _items_of_type(self, obj, item_type):
        items = [
            item for item in obj.detail_items.all() if item.item_type == item_type
        ]
        return FocusAreaDetailItemSerializer(items, many=True).data

    def get_career_paths(self, obj):
        return self._items_of_type(obj, "career")

    def get_research_themes(self, obj):
        return self._items_of_type(obj, "theme")

    class Meta:
        model = FocusArea
        fields = (
            "id",
            "sort_order",
            "code",
            "title",
            "slug",
            "description",
            "accent_color",
            "image",
            "overview_heading",
            "overview_intro",
            "facility_heading",
            "facility_intro",
            "curriculum_heading",
            "curriculum_intro",
            "learning_heading",
            "learning_intro",
            "careers_heading",
            "careers_intro",
            "research_heading",
            "research_intro",
            "research_question",
            "research_overview",
            "career_paths",
            "research_themes",
        )


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "sort_order", "code", "title", "credits", "semester")


class FocusCourseSerializer(CourseSerializer):
    year = serializers.IntegerField(source="curriculum_year.year", read_only=True)
    year_theme = serializers.CharField(
        source="curriculum_year.theme", read_only=True
    )

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ("year", "year_theme")


class CurriculumYearSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = CurriculumYear
        fields = (
            "id",
            "sort_order",
            "year",
            "theme",
            "credit_count",
            "description",
            "courses",
        )


class ResearchProjectSerializer(ImageSerializerMixin, serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_field = "image"
    focus_areas = FocusAreaSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchProject
        fields = (
            "id",
            "sort_order",
            "title",
            "slug",
            "summary",
            "body",
            "image",
            "focus_areas",
            "published_at",
        )


class PartnerSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        return image_url(obj.logo, self.context.get("request"))

    class Meta:
        model = Partner
        fields = ("id", "sort_order", "name", "partner_type", "website", "logo")


class OpportunityFocusAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocusArea
        fields = ("code", "title", "slug", "accent_color")


class OpportunitySerializer(serializers.ModelSerializer):
    partner = PartnerSerializer(read_only=True)
    focus_areas = OpportunityFocusAreaSerializer(many=True, read_only=True)
    announcement_image = serializers.SerializerMethodField()
    opportunity_type_label = serializers.CharField(
        source="get_opportunity_type_display",
        read_only=True,
    )

    def get_announcement_image(self, obj):
        return image_url(
            obj.announcement_image,
            self.context.get("request"),
        )

    class Meta:
        model = Opportunity
        fields = (
            "id",
            "sort_order",
            "title",
            "slug",
            "opportunity_type",
            "opportunity_type_label",
            "partner",
            "announcement_image",
            "focus_areas",
            "summary",
            "body",
            "location",
            "application_deadline",
            "application_url",
            "published_at",
            "is_featured",
        )


class FacilitySerializer(ImageSerializerMixin, serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    availability_label = serializers.CharField(
        source="get_availability_status_display",
        read_only=True,
    )
    image_field = "image"

    class Meta:
        model = Facility
        fields = (
            "id",
            "sort_order",
            "name",
            "description",
            "reference_url",
            "availability_status",
            "availability_label",
            "image",
        )


class FocusAreaDetailItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocusAreaDetailItem
        fields = ("id", "sort_order", "title", "description")


class FocusAreaDetailSerializer(FocusAreaSerializer):
    courses = FocusCourseSerializer(many=True, read_only=True)
    facilities = FacilitySerializer(many=True, read_only=True)
    outcomes = serializers.SerializerMethodField()
    learning_activities = serializers.SerializerMethodField()
    research_projects = serializers.SerializerMethodField()

    def get_outcomes(self, obj):
        return self._items_of_type(obj, "outcome")

    def get_learning_activities(self, obj):
        return self._items_of_type(obj, "activity")

    def get_research_projects(self, obj):
        projects = obj.research_projects.filter(is_published=True)
        return ResearchProjectSerializer(
            projects,
            many=True,
            context=self.context,
        ).data

    class Meta(FocusAreaSerializer.Meta):
        fields = FocusAreaSerializer.Meta.fields + (
            "courses",
            "facilities",
            "outcomes",
            "learning_activities",
            "research_projects",
        )


class FacultyWorkItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return image_url(obj.image, self.context.get("request"))

    class Meta:
        model = FacultyWorkItem
        fields = (
            "id",
            "sort_order",
            "badge",
            "title",
            "meta",
            "summary",
            "image",
            "link_url",
            "link_label",
        )


class FacultyMemberSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    work_items = FacultyWorkItemSerializer(many=True, read_only=True)
    focus_areas = FocusAreaSerializer(many=True, read_only=True)
    research_interests = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    courses_taught = serializers.SerializerMethodField()
    publications = serializers.SerializerMethodField()

    def get_photo(self, obj):
        return image_url(obj.photo, self.context.get("request"))

    @staticmethod
    def _lines(value):
        """Authors enter one item per line; the API returns a clean list."""
        return [line.strip() for line in (value or "").splitlines() if line.strip()]

    def get_research_interests(self, obj):
        return self._lines(obj.research_interests)

    def get_education(self, obj):
        return self._lines(obj.education)

    def get_courses_taught(self, obj):
        return self._lines(obj.courses_taught)

    def get_publications(self, obj):
        return self._lines(obj.publications)

    class Meta:
        model = FacultyMember
        fields = (
            "id",
            "sort_order",
            "name",
            "slug",
            "credentials",
            "role",
            "statement",
            "bio",
            "email",
            "phone",
            "office",
            "profile_url",
            "research_interests",
            "education",
            "courses_taught",
            "publications",
            "work_items",
            "photo",
            "focus_areas",
        )


class NewsEventSerializer(ImageSerializerMixin, serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    image_field = "image"

    def get_body(self, obj):
        """Flatten the StreamField into blocks the frontend can render.

        Sent as typed data rather than a slab of HTML so each block keeps its
        own markup and styling on the page, and images and documents arrive as
        resolved URLs.
        """
        request = self.context.get("request")
        blocks = []

        for child in obj.body:
            value = child.value

            if child.block_type == "heading":
                blocks.append({"type": "heading", "value": str(value)})
            elif child.block_type == "paragraph":
                blocks.append(
                    {"type": "paragraph", "value": expand_db_html(value.source)}
                )
            elif child.block_type == "image":
                image = value.get("image")
                if not image:
                    continue
                blocks.append(
                    {
                        "type": "image",
                        "url": image_url(image, request),
                        "caption": value.get("caption", ""),
                        "alt_text": value.get("alt_text", ""),
                    }
                )
            elif child.block_type == "quote":
                blocks.append(
                    {
                        "type": "quote",
                        "value": value.get("text", ""),
                        "attribution": value.get("attribution", ""),
                    }
                )
            elif child.block_type == "video":
                blocks.append(
                    {
                        "type": "video",
                        "url": value.get("url", ""),
                        "caption": value.get("caption", ""),
                    }
                )
            elif child.block_type == "document":
                document = value.get("document")
                if not document:
                    continue
                url = document.url
                blocks.append(
                    {
                        "type": "document",
                        "url": request.build_absolute_uri(url) if request else url,
                        "label": value.get("label", "") or document.title,
                        "filename": document.filename,
                    }
                )

        return blocks

    class Meta:
        model = NewsEvent
        fields = (
            "id",
            "sort_order",
            "content_type",
            "category",
            "title",
            "slug",
            "excerpt",
            "body",
            "image",
            "event_date",
            "published_at",
        )


class ProgramSettingsSerializer(serializers.ModelSerializer):
    hero_image = serializers.SerializerMethodField()

    def get_hero_image(self, obj):
        return image_url(obj.hero_image, self.context.get("request"))

    class Meta:
        model = ProgramSettings
        fields = (
            "program_name",
            "program_short_name",
            "established_year",
            "hero_title",
            "hero_emphasis",
            "hero_description",
            "hero_image",
            "what_is_me_eyebrow",
            "what_is_me_heading",
            "what_is_me_intro",
            "focus_section_eyebrow",
            "focus_section_heading",
            "focus_section_intro",
            "why_section_eyebrow",
            "why_section_heading",
            "why_section_intro",
            "partners_section_eyebrow",
            "partners_section_heading",
            "partners_section_intro",
            "research_hero_eyebrow",
            "research_hero_title",
            "research_hero_description",
            "research_quote",
            "research_quote_attribution",
            "research_areas_eyebrow",
            "research_areas_heading",
            "research_areas_intro",
            "research_projects_eyebrow",
            "research_projects_heading",
            "research_projects_intro",
            "research_collaboration_eyebrow",
            "research_collaboration_heading",
            "research_area_projects_eyebrow",
            "research_area_projects_intro",
            "research_boundaries_eyebrow",
            "research_boundaries_heading",
            "vision",
            "mission_one",
            "mission_two",
            "program_years",
            "credit_hours",
            "address",
            "email",
            "phone",
            "facebook_url",
            "telegram_url",
            "youtube_url",
            "linkedin_url",
            "application_url",
        )


class InquirySerializer(serializers.ModelSerializer):
    website = serializers.CharField(
        required=False, allow_blank=True, write_only=True, max_length=200
    )

    class Meta:
        model = Inquiry
        fields = (
            "id",
            "inquiry_type",
            "name",
            "email",
            "phone",
            "organization",
            "subject",
            "message",
            "website",
            "created_at",
        )
        read_only_fields = ("id", "created_at")

    def validate_website(self, value):
        if value:
            raise serializers.ValidationError("Unable to submit this form.")
        return value

    def create(self, validated_data):
        validated_data.pop("website", None)
        return super().create(validated_data)
