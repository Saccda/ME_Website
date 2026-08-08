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


# Sizes matched to the boxes these images actually land in. Serving the
# original means a 5712px photograph is downloaded to fill a 460px card, and
# the browser does the cropping the CMS should have done.
CARD_IMAGE = "fill-900x563"  # 16:10, the news and event card crop
WIDE_IMAGE = "width-2400"  # full-bleed story lead
BODY_IMAGE = "width-1600"  # a figure inside the story band
ROW_IMAGE = "fill-1200x800"  # 3:2, the image-row crop
THUMB_IMAGE = "fill-600x400"  # 3:2, a gallery thumbnail


def document_url(document, request=None):
    if not document:
        return None
    url = document.url
    return request.build_absolute_uri(url) if request else url


def rendition_url(image, spec, request=None):
    """A resized copy, generated and cached by Wagtail on first request.

    Falls back to the original if the source cannot be processed -- a missing
    file or a format Pillow cannot open -- so a bad upload degrades to a large
    image rather than a broken one.
    """
    if not image:
        return None
    try:
        url = image.get_rendition(spec).url
    except (OSError, ValueError):
        return image_url(image, request)
    return request.build_absolute_uri(url) if request else url


class ImageSerializerMixin:
    def get_image(self, obj):
        request = self.context.get("request")
        image = getattr(obj, self.image_field, None)
        return image_url(image, request)


def story_blocks(stream_value, request=None):
    """Flatten a StreamField into typed blocks the frontend can render.

    Sent as typed data rather than a slab of HTML, so each block keeps its own
    markup and styling on the page and images and documents arrive as resolved
    URLs. Shared by news stories and research projects; the structured blocks
    at the end only ever appear in a research body.
    """
    blocks = []

    for child in stream_value:
        value = child.value
        kind = child.block_type

        if kind == "heading":
            blocks.append({"type": "heading", "value": str(value)})

        elif kind == "paragraph":
            blocks.append({"type": "paragraph", "value": expand_db_html(value.source)})

        elif kind == "image":
            image = value.get("image")
            if not image:
                continue
            blocks.append(
                {
                    "type": "image",
                    "url": rendition_url(image, BODY_IMAGE, request),
                    "caption": value.get("caption", ""),
                    "alt_text": value.get("alt_text", ""),
                }
            )

        elif kind == "gallery":
            images = [
                {
                    "url": rendition_url(entry.get("image"), ROW_IMAGE, request),
                    "alt_text": entry.get("alt_text", ""),
                }
                for entry in value.get("images", [])
                if entry.get("image")
            ]
            if not images:
                continue
            blocks.append(
                {
                    "type": "gallery",
                    "images": images,
                    "caption": value.get("caption", ""),
                }
            )

        elif kind == "media_gallery":
            items = []
            for item in value.get("items", []):
                if item.block_type == "image":
                    image = item.value.get("image")
                    if not image:
                        continue
                    items.append(
                        {
                            "kind": "image",
                            "thumb": rendition_url(image, THUMB_IMAGE, request),
                            "url": rendition_url(image, BODY_IMAGE, request),
                            "file_url": None,
                            "caption": item.value.get("caption", ""),
                            "alt_text": item.value.get("alt_text", ""),
                        }
                    )
                elif item.block_type == "video":
                    file_url = document_url(item.value.get("video_file"), request)
                    if not item.value.get("url") and not file_url:
                        continue
                    items.append(
                        {
                            "kind": "video",
                            "url": item.value.get("url", "") or file_url,
                            "file_url": file_url,
                            "thumb": rendition_url(
                                item.value.get("poster"), THUMB_IMAGE, request
                            ),
                            "caption": item.value.get("caption", ""),
                            "alt_text": "",
                        }
                    )
            if not items:
                continue
            blocks.append(
                {
                    "type": "media_gallery",
                    "heading": value.get("heading", ""),
                    "caption": value.get("caption", ""),
                    "items": items,
                }
            )

        elif kind == "collection_gallery":
            from wagtail.images import get_image_model

            collection_id = value.get("collection")
            if not collection_id:
                continue
            images = (
                get_image_model()
                .objects.filter(collection_id=collection_id)
                .order_by("pk")
            )
            items = [
                {
                    "kind": "image",
                    "thumb": rendition_url(image, THUMB_IMAGE, request),
                    "url": rendition_url(image, BODY_IMAGE, request),
                    "file_url": None,
                    "caption": "",
                    "alt_text": image.title,
                }
                for image in images
            ]
            if not items:
                continue
            blocks.append(
                {
                    "type": "media_gallery",
                    "heading": value.get("heading", ""),
                    "caption": value.get("caption", ""),
                    "items": items,
                }
            )

        elif kind == "quote":
            blocks.append(
                {
                    "type": "quote",
                    "value": value.get("text", ""),
                    "attribution": value.get("attribution", ""),
                }
            )

        elif kind == "video":
            video_file = value.get("video_file")
            url = value.get("url", "")
            if not url and not video_file:
                continue
            blocks.append(
                {
                    "type": "video",
                    "url": url,
                    "file_url": document_url(video_file, request),
                    "caption": value.get("caption", ""),
                    "poster": rendition_url(value.get("poster"), BODY_IMAGE, request),
                }
            )

        elif kind == "document":
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

        elif kind == "key_facts":
            facts = [
                {"label": fact.get("label", ""), "value": fact.get("value", "")}
                for fact in value.get("facts", [])
                if fact.get("label") or fact.get("value")
            ]
            if not facts:
                continue
            blocks.append(
                {
                    "type": "key_facts",
                    "heading": value.get("heading", ""),
                    "facts": facts,
                }
            )

        elif kind == "stats":
            stats = [
                {"value": stat.get("value", ""), "label": stat.get("label", "")}
                for stat in value.get("stats", [])
                if stat.get("value")
            ]
            if not stats:
                continue
            blocks.append(
                {
                    "type": "stats",
                    "heading": value.get("heading", ""),
                    "stats": stats,
                }
            )

        elif kind == "steps":
            steps = [
                {
                    "title": step.get("title", ""),
                    "description": step.get("description", ""),
                }
                for step in value.get("steps", [])
                if step.get("title")
            ]
            if not steps:
                continue
            blocks.append(
                {
                    "type": "steps",
                    "heading": value.get("heading", ""),
                    "steps": steps,
                }
            )

        elif kind == "table":
            table = value.get("table") or {}
            rows = [row.get("data", []) for row in (table.get("data") or [])]
            if not rows:
                continue
            blocks.append(
                {
                    "type": "table",
                    "heading": value.get("heading", ""),
                    "caption": value.get("caption", ""),
                    "first_row_is_header": bool(
                        table.get("first_row_is_table_header")
                    ),
                    "first_col_is_header": bool(table.get("first_col_is_header")),
                    "rows": rows,
                }
            )

        elif kind == "callout":
            text = value.get("text", "")
            if not text:
                continue
            blocks.append(
                {
                    "type": "callout",
                    "label": value.get("label", ""),
                    "value": text,
                }
            )

        elif kind == "references":
            entries = [
                {
                    "citation": entry.get("citation", ""),
                    "url": entry.get("url", "") or "",
                }
                for entry in value.get("entries", [])
                if entry.get("citation")
            ]
            if not entries:
                continue
            blocks.append(
                {
                    "type": "references",
                    "heading": value.get("heading", ""),
                    "entries": entries,
                }
            )

    return blocks


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
    body = serializers.SerializerMethodField()

    def get_body(self, obj):
        return story_blocks(obj.body, self.context.get("request"))

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


class NewsEventSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_wide = serializers.SerializerMethodField()
    card_media = serializers.SerializerMethodField()
    has_video = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()

    def get_image(self, obj):
        return rendition_url(obj.image, CARD_IMAGE, self.context.get("request"))

    def get_image_wide(self, obj):
        return rendition_url(obj.image, WIDE_IMAGE, self.context.get("request"))

    def get_card_media(self, obj):
        """Stills for the card slideshow, drawn from the story itself.

        Taken from the lead image and then the pictures in the body, so an
        author gets a slideshow by writing the story rather than by filling in
        a second set of fields. Capped, because a card is a preview.
        """
        request = self.context.get("request")
        urls = []

        def add(image):
            url = rendition_url(image, CARD_IMAGE, request)
            if url and url not in urls:
                urls.append(url)

        add(obj.image)
        for child in obj.body:
            if len(urls) >= 5:
                break
            if child.block_type == "image":
                add(child.value.get("image"))
            elif child.block_type == "gallery":
                for entry in child.value.get("images", []):
                    add(entry.get("image"))
            elif child.block_type == "media_gallery":
                for item in child.value.get("items", []):
                    if item.block_type == "image":
                        add(item.value.get("image"))

        return urls[:5]

    def get_has_video(self, obj):
        for child in obj.body:
            if child.block_type == "video":
                return True
            if child.block_type == "media_gallery":
                for item in child.value.get("items", []):
                    if item.block_type == "video":
                        return True
        return False

    def get_body(self, obj):
        return story_blocks(obj.body, self.context.get("request"))

    class Meta:
        model = NewsEvent
        fields = (
            "id",
            "sort_order",
            "content_type",
            "category",
            "title",
            "slug",
            "author",
            "excerpt",
            "body",
            "image",
            "image_wide",
            "card_media",
            "has_video",
            "announce",
            "announcement_cta",
            "event_date",
            "event_end_date",
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
