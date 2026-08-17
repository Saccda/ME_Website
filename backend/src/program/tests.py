import json
import tempfile
from datetime import timedelta

from django.core import mail
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.core.files.base import ContentFile
from wagtail.documents import get_document_model
from wagtail.images import get_image_model
from wagtail.images.tests.utils import get_test_image_file
from wagtail.models import Collection, Site

from .management.commands.seed_article_bank import ARTICLES
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
    NewsEventGalleryImage,
    Opportunity,
    Partner,
    ProgramSettings,
    ResearchProject,
)


class PublicApiTests(TestCase):
    def setUp(self):
        self.site = Site.objects.filter(is_default_site=True).first()
        ProgramSettings.objects.get_or_create(site=self.site)

    def test_health_endpoint(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_home_endpoint(self):
        response = self.client.get(reverse("home-data"))
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["settings"]["program_short_name"], "ME")
        self.assertIn("focus_areas", body)
        self.assertIn("partners", body)
        self.assertIn("opportunities", body)
        self.assertEqual(
            body["settings"]["research_hero_eyebrow"], "Research at ME RUPP"
        )
        self.assertEqual(
            body["settings"]["research_areas_heading"],
            "Investigate our four research areas",
        )

    def test_home_endpoint_exposes_focus_area_research_editorial(self):
        focus = FocusArea.objects.create(
            code="TES",
            title="Thermofluid and Energy System",
            slug="thermofluid-and-energy-system",
            description="Engineer systems that use energy responsibly.",
            research_question="How can energy systems work more efficiently?",
            research_overview="TES research investigates heat, fluids, and energy conversion.",
        )
        FocusAreaDetailItem.objects.create(
            focus_area=focus,
            item_type="theme",
            title="Renewable energy and storage",
        )
        FocusAreaDetailItem.objects.create(
            focus_area=focus,
            item_type="career",
            title="Energy Engineer",
        )

        response = self.client.get(reverse("home-data"))
        self.assertEqual(response.status_code, 200)
        area = response.json()["focus_areas"][0]
        self.assertEqual(
            area["research_question"], "How can energy systems work more efficiently?"
        )
        self.assertEqual(
            area["research_overview"],
            "TES research investigates heat, fluids, and energy conversion.",
        )
        self.assertEqual(
            [theme["title"] for theme in area["research_themes"]],
            ["Renewable energy and storage"],
        )
        self.assertEqual(
            [career["title"] for career in area["career_paths"]], ["Energy Engineer"]
        )

    def test_home_endpoint_only_returns_current_published_opportunities(self):
        partner = Partner.objects.create(
            name="Industry Partner",
            partner_type="industry",
        )
        current = Opportunity.objects.create(
            title="Graduate Mechanical Engineer",
            slug="graduate-mechanical-engineer",
            partner=partner,
            summary="An entry-level engineering opportunity.",
            application_deadline=timezone.localdate() + timedelta(days=14),
            is_published=True,
        )
        Opportunity.objects.create(
            title="Expired Internship",
            slug="expired-internship",
            partner=partner,
            summary="An opportunity whose deadline has passed.",
            application_deadline=timezone.localdate() - timedelta(days=1),
            is_published=True,
        )
        Opportunity.objects.create(
            title="Draft Scholarship",
            slug="draft-scholarship",
            partner=partner,
            summary="An unpublished opportunity.",
            is_published=False,
        )

        response = self.client.get(reverse("home-data"))
        self.assertEqual(response.status_code, 200)
        opportunities = response.json()["opportunities"]
        self.assertEqual([item["slug"] for item in opportunities], [current.slug])
        self.assertIsNone(opportunities[0]["announcement_image"])

    def test_focus_area_detail_endpoint(self):
        focus = FocusArea.objects.create(
            code="DMP",
            title="Design and Manufacturing Process",
            slug="design-and-manufacturing-process",
            description="Turn ideas into manufactured products.",
        )
        year = CurriculumYear.objects.create(
            year=2,
            theme="Core engineering systems",
            credit_count=36,
        )
        course = Course.objects.create(
            curriculum_year=year,
            code="ME 219",
            title="Materials & Manufacturing",
            credits=4,
        )
        course.focus_areas.add(focus)
        facility = Facility.objects.create(
            name="CNC Machine",
            description="Precision manufacturing equipment.",
        )
        facility.focus_areas.add(focus)
        FocusAreaDetailItem.objects.create(
            focus_area=focus,
            item_type="activity",
            title="CNC workshop practice",
            description="Plan and machine a component safely.",
        )
        project = ResearchProject.objects.create(
            title="Automated Cooling",
            slug="automated-cooling",
            summary="A cross-disciplinary cooling and control project.",
        )
        project.focus_areas.add(focus)

        response = self.client.get(
            reverse("focus-area-detail", args=(focus.slug,))
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["code"], "DMP")
        self.assertEqual(body["courses"][0]["code"], "ME 219")
        self.assertEqual(body["facilities"][0]["name"], "CNC Machine")
        self.assertEqual(
            body["learning_activities"][0]["title"], "CNC workshop practice"
        )
        self.assertEqual(body["research_projects"][0]["focus_areas"][0]["code"], "DMP")

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_faculty_endpoint_exposes_profile_fields_as_lists(self):
        focus = FocusArea.objects.create(
            code="DMP",
            title="Design and Manufacturing Process",
            slug="design-and-manufacturing-process",
            description="Focus area.",
        )
        member = FacultyMember.objects.create(
            name="Sok Dara",
            credentials="Ph.D.",
            role="Head of Mechanical Engineering",
            bio="Teaches design and manufacturing.",
            email="sok.dara@example.org",
            phone="+855 12 000 000",
            office="Engineering Building, Room 204",
            research_interests="Additive manufacturing\n\nPrecision machining\n",
            education="Ph.D. Mechanical Engineering, 2016\nM.Eng. Manufacturing, 2011",
            courses_taught="Manufacturing Processes",
            publications="Dara, S. (2023) A paper title. Journal 10:1-12.",
            profile_url="https://scholar.example.org/dara",
        )
        member.focus_areas.add(focus)

        response = self.client.get("/api/v1/faculty/")
        self.assertEqual(response.status_code, 200)
        body = response.json()["results"][0]

        self.assertEqual(body["slug"], "sok-dara")
        self.assertEqual(body["credentials"], "Ph.D.")
        self.assertEqual(body["office"], "Engineering Building, Room 204")
        self.assertEqual(body["phone"], "+855 12 000 000")
        self.assertEqual(body["profile_url"], "https://scholar.example.org/dara")
        # Blank lines and stray whitespace must not become empty list entries.
        self.assertEqual(
            body["research_interests"],
            ["Additive manufacturing", "Precision machining"],
        )
        self.assertEqual(len(body["education"]), 2)
        self.assertEqual(body["courses_taught"], ["Manufacturing Processes"])
        self.assertEqual(len(body["publications"]), 1)
        self.assertEqual(body["focus_areas"][0]["code"], "DMP")

    def test_faculty_profile_lists_default_to_empty(self):
        FacultyMember.objects.create(name="Chan Sophea", role="Lecturer")
        response = self.client.get("/api/v1/faculty/")
        body = response.json()["results"][0]
        for field in (
            "research_interests",
            "education",
            "courses_taught",
            "publications",
        ):
            self.assertEqual(body[field], [], field)

    def test_inquiry_submission(self):
        response = self.client.post(
            reverse("inquiry-create"),
            data={
                "inquiry_type": "admission",
                "name": "Prospective Student",
                "email": "student@example.com",
                "subject": "Admission information",
                "message": "Please share the application requirements.",
                "website": "",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Inquiry.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_honeypot_rejects_spam(self):
        response = self.client.post(
            reverse("inquiry-create"),
            data={
                "name": "Spam",
                "email": "spam@example.com",
                "subject": "Spam",
                "message": "Spam message",
                "website": "https://spam.example.com",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Inquiry.objects.count(), 0)


class FacultyWorkItemTests(TestCase):
    """Selected work cards are authored per member and exposed in order."""

    def test_work_items_are_serialized_in_sort_order(self):
        member = FacultyMember.objects.create(
            name="Sok Dara",
            role="Lecturer",
        )
        FacultyWorkItem.objects.create(
            member=member,
            sort_order=2,
            badge="Mentorship",
            title="Supervising final-year capstone teams",
            meta="Teaching · Supervision",
            summary="Guiding student teams through the capstone process.",
            link_url="/curriculum",
            link_label="See the curriculum",
        )
        FacultyWorkItem.objects.create(
            member=member,
            sort_order=1,
            badge="Research project",
            title="Automated cooling",
            link_url="https://example.org/project",
        )

        response = self.client.get(reverse("faculty-list"))
        self.assertEqual(response.status_code, 200)
        items = response.json()["results"][0]["work_items"]
        self.assertEqual(
            [item["title"] for item in items],
            ["Automated cooling", "Supervising final-year capstone teams"],
        )
        self.assertEqual(items[1]["badge"], "Mentorship")
        self.assertEqual(items[1]["link_label"], "See the curriculum")

    def test_member_without_work_items_returns_an_empty_list(self):
        FacultyMember.objects.create(name="Chan Sopheak", role="Lecturer")

        response = self.client.get(reverse("faculty-list"))
        self.assertEqual(response.json()["results"][0]["work_items"], [])


class StoryBodyTests(TestCase):
    """Story bodies are sent as typed blocks, not one slab of HTML."""

    def setUp(self):
        cache.clear()

    def test_body_blocks_are_serialized_by_type(self):
        NewsEvent.objects.create(
            content_type="news",
            category="Projects & Community",
            title="From site assessment to long-term support",
            slug="site-assessment-to-long-term-support",
            excerpt="Working with a farm to install an automated system.",
            body=json.dumps(
                [
                    {"type": "heading", "value": "What we built"},
                    {"type": "paragraph", "value": "<p>An automated system.</p>"},
                    {
                        "type": "quote",
                        "value": {
                            "text": "The students handled the commissioning.",
                            "attribution": "Site supervisor",
                        },
                    },
                    {
                        "type": "video",
                        "value": {
                            "url": "https://www.youtube.com/watch?v=abc123",
                            "caption": "Commissioning day",
                        },
                    },
                ]
            ),
        )

        response = self.client.get(reverse("news-list"))
        self.assertEqual(response.status_code, 200)
        story = response.json()["results"][0]
        self.assertEqual(story["category"], "Projects & Community")

        blocks = story["body"]
        self.assertEqual(
            [block["type"] for block in blocks],
            ["heading", "paragraph", "quote", "video"],
        )
        self.assertEqual(blocks[0]["value"], "What we built")
        self.assertIn("An automated system.", blocks[1]["value"])
        self.assertEqual(blocks[2]["attribution"], "Site supervisor")
        self.assertEqual(blocks[3]["caption"], "Commissioning day")

    def test_card_and_lead_images_are_sized_renditions(self):
        """Cards must not be served the full-size original.

        Uploads and renditions go to a temporary directory so the suite does
        not leave test images behind in the project's media folder.
        """
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                image = get_image_model().objects.create(
                    title="Laboratory",
                    file=get_test_image_file(size=(3000, 2000)),
                )
                NewsEvent.objects.create(
                    content_type="news",
                    title="A story with a photograph",
                    slug="story-with-a-photograph",
                    excerpt="It has a picture.",
                    image=image,
                )

                story = self.client.get(reverse("news-list")).json()["results"][0]
                self.assertNotIn("original_images", story["image"])
                self.assertNotIn("original_images", story["image_wide"])
                self.assertNotEqual(story["image"], story["image_wide"])

                card = image.get_rendition("fill-900x563")
                self.assertEqual((card.width, card.height), (900, 563))
                self.assertEqual(image.get_rendition("width-2400").width, 2400)

    def test_media_gallery_and_card_media(self):
        """Galleries carry images and videos; cards get stills from the story."""
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                Image = get_image_model()
                lead = Image.objects.create(
                    title="Lead", file=get_test_image_file(size=(2000, 1400))
                )
                shot = Image.objects.create(
                    title="Day one", file=get_test_image_file(size=(2000, 1400))
                )
                NewsEvent.objects.create(
                    content_type="news",
                    title="A three day activity",
                    slug="a-three-day-activity",
                    excerpt="It ran over several days.",
                    image=lead,
                    body=json.dumps(
                        [
                            {
                                "type": "media_gallery",
                                "value": {
                                    "heading": "Day one",
                                    "caption": "The whole set.",
                                    "items": [
                                        {
                                            "type": "image",
                                            "value": {
                                                "image": shot.pk,
                                                "caption": "Setting up",
                                                "alt_text": "Students setting up",
                                            },
                                        },
                                        {
                                            "type": "video",
                                            "value": {
                                                "url": "https://youtu.be/abc123",
                                                "caption": "Time lapse",
                                            },
                                        },
                                    ],
                                },
                            }
                        ]
                    ),
                )

                story = self.client.get(reverse("news-list")).json()["results"][0]

                gallery = story["body"][0]
                self.assertEqual(gallery["type"], "media_gallery")
                self.assertEqual(gallery["heading"], "Day one")
                self.assertEqual(
                    [item["kind"] for item in gallery["items"]], ["image", "video"]
                )
                self.assertIsNotNone(gallery["items"][0]["thumb"])
                self.assertEqual(gallery["items"][1]["url"], "https://youtu.be/abc123")

                # The card slideshow picks up the lead plus the gallery still.
                self.assertEqual(len(story["card_media"]), 2)
                self.assertTrue(story["has_video"])

    def test_story_without_video_is_not_flagged(self):
        NewsEvent.objects.create(
            content_type="news",
            title="A story with no video",
            slug="a-story-with-no-video",
            excerpt="Text only.",
        )
        story = self.client.get(reverse("news-list")).json()["results"][0]
        self.assertFalse(story["has_video"])
        self.assertEqual(story["card_media"], [])

    def test_gallery_without_images_is_dropped(self):
        NewsEvent.objects.create(
            content_type="news",
            title="A story with an unfilled image row",
            slug="story-with-unfilled-image-row",
            excerpt="The author added the block but chose no pictures.",
            body=json.dumps(
                [
                    {"type": "gallery", "value": {"images": [], "caption": "Row"}},
                    {"type": "heading", "value": "Still here"},
                ]
            ),
        )

        response = self.client.get(reverse("news-list"))
        blocks = response.json()["results"][0]["body"]
        self.assertEqual([block["type"] for block in blocks], ["heading"])

    def test_empty_body_serializes_as_an_empty_list(self):
        NewsEvent.objects.create(
            content_type="event",
            title="Laboratory open house",
            slug="laboratory-open-house",
            excerpt="Tour the laboratories.",
        )

        response = self.client.get(reverse("news-list"))
        self.assertEqual(response.json()["results"][0]["body"], [])


class ResearchBodyTests(TestCase):
    """A research write-up carries structures a news story does not."""

    def test_structured_blocks_are_serialized(self):
        ResearchProject.objects.create(
            title="Metal Recycling",
            slug="metal-recycling",
            summary="Recovering workshop metal for teaching stock.",
            body=json.dumps(
                [
                    {
                        "type": "key_facts",
                        "value": {
                            "heading": "Project facts",
                            "facts": [
                                {"label": "Team", "value": "Four students"},
                                {"label": "Status", "value": "Ongoing"},
                            ],
                        },
                    },
                    {
                        "type": "stats",
                        "value": {
                            "heading": "Results",
                            "stats": [
                                {"value": "42%", "label": "Material recovered"},
                                {"value": "1.8 kW", "label": "Furnace draw"},
                            ],
                        },
                    },
                    {
                        "type": "steps",
                        "value": {
                            "heading": "Method",
                            "steps": [
                                {"title": "Collect", "description": "Sort by alloy."},
                                {"title": "Melt", "description": ""},
                            ],
                        },
                    },
                    {
                        "type": "callout",
                        "value": {"label": "Safety", "text": "Hot metal handling."},
                    },
                    {
                        "type": "references",
                        "value": {
                            "heading": "Publications",
                            "entries": [
                                {
                                    "citation": "Dara, S. (2026) Recovery rates.",
                                    "url": "https://example.org/paper",
                                }
                            ],
                        },
                    },
                ]
            ),
        )

        response = self.client.get(reverse("research-list"))
        self.assertEqual(response.status_code, 200)
        blocks = response.json()["results"][0]["body"]

        self.assertEqual(
            [block["type"] for block in blocks],
            ["key_facts", "stats", "steps", "callout", "references"],
        )
        self.assertEqual(blocks[0]["facts"][1], {"label": "Status", "value": "Ongoing"})
        self.assertEqual(blocks[1]["stats"][0]["value"], "42%")
        self.assertEqual(blocks[2]["steps"][1]["description"], "")
        self.assertEqual(blocks[3]["value"], "Hot metal handling.")
        self.assertEqual(blocks[4]["entries"][0]["url"], "https://example.org/paper")

    def test_table_block_reports_its_header_flags(self):
        ResearchProject.objects.create(
            title="Load Monitoring",
            slug="load-monitoring",
            summary="Appliance-level energy use.",
            body=json.dumps(
                [
                    {
                        "type": "table",
                        "value": {
                            "heading": "Test conditions",
                            "caption": "Measured at 25C.",
                            "table": {
                                "first_row_is_table_header": True,
                                "first_col_is_header": False,
                                "data": [
                                    {"data": ["Load", "Power"]},
                                    {"data": ["Kettle", "2.0 kW"]},
                                ],
                            },
                        },
                    }
                ]
            ),
        )

        block = self.client.get(reverse("research-list")).json()["results"][0]["body"][0]
        self.assertEqual(block["type"], "table")
        self.assertTrue(block["first_row_is_header"])
        self.assertFalse(block["first_col_is_header"])
        self.assertEqual(block["rows"], [["Load", "Power"], ["Kettle", "2.0 kW"]])
        self.assertEqual(block["caption"], "Measured at 25C.")

    def test_empty_research_body_serializes_as_an_empty_list(self):
        ResearchProject.objects.create(
            title="Sugarcane Particle Board",
            slug="sugarcane-particle-board",
            summary="Residue as an engineered material.",
        )
        story = self.client.get(reverse("research-list")).json()["results"][0]
        self.assertEqual(story["body"], [])

    def test_structured_blocks_without_content_are_dropped(self):
        ResearchProject.objects.create(
            title="Draft Project",
            slug="draft-project",
            summary="Blocks added but not filled in.",
            body=json.dumps(
                [
                    {"type": "stats", "value": {"heading": "Results", "stats": []}},
                    {"type": "heading", "value": "Still here"},
                ]
            ),
        )
        blocks = self.client.get(reverse("research-list")).json()["results"][0]["body"]
        self.assertEqual([block["type"] for block in blocks], ["heading"])


class MediaAndDateRangeTests(TestCase):
    """Uploaded video, collection galleries, and multi-day events."""

    def setUp(self):
        cache.clear()

    def test_video_block_exposes_an_uploaded_file(self):
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                document = get_document_model().objects.create(
                    title="Site walkthrough",
                    file=ContentFile(b"not really a video", name="walkthrough.mp4"),
                )
                NewsEvent.objects.create(
                    content_type="news",
                    title="A story with an uploaded clip",
                    slug="story-with-uploaded-clip",
                    excerpt="Short clip hosted here.",
                    body=json.dumps(
                        [
                            {
                                "type": "video",
                                "value": {
                                    "url": "",
                                    "video_file": document.pk,
                                    "caption": "Walkthrough",
                                },
                            }
                        ]
                    ),
                )

                block = self.client.get(reverse("news-list")).json()["results"][0][
                    "body"
                ][0]
                self.assertEqual(block["type"], "video")
                self.assertEqual(block["url"], "")
                self.assertIn("walkthrough", block["file_url"])

    def test_video_block_with_neither_link_nor_file_is_dropped(self):
        NewsEvent.objects.create(
            content_type="news",
            title="A story with an empty video block",
            slug="story-with-empty-video",
            excerpt="Author added the block but filled nothing in.",
            body=json.dumps(
                [
                    {"type": "video", "value": {"url": "", "caption": ""}},
                    {"type": "heading", "value": "Still here"},
                ]
            ),
        )
        blocks = self.client.get(reverse("news-list")).json()["results"][0]["body"]
        self.assertEqual([block["type"] for block in blocks], ["heading"])

    def test_collection_gallery_returns_every_image_in_the_collection(self):
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                collection = Collection.get_first_root_node().add_child(
                    name="Learning Express 2026"
                )
                Image = get_image_model()
                for index in range(3):
                    Image.objects.create(
                        title=f"Day {index + 1}",
                        collection=collection,
                        file=get_test_image_file(size=(900, 600)),
                    )
                # An image outside the collection must not appear.
                Image.objects.create(
                    title="Unrelated", file=get_test_image_file(size=(900, 600))
                )

                NewsEvent.objects.create(
                    content_type="news",
                    title="A three day activity",
                    slug="a-three-day-activity",
                    excerpt="Photographs uploaded in one go.",
                    body=json.dumps(
                        [
                            {
                                "type": "collection_gallery",
                                "value": {
                                    "heading": "Every day",
                                    "collection": str(collection.pk),
                                    "caption": "Uploaded as a set.",
                                },
                            }
                        ]
                    ),
                )

                block = self.client.get(reverse("news-list")).json()["results"][0][
                    "body"
                ][0]
                # Serialized as a media_gallery so the frontend needs no second
                # renderer.
                self.assertEqual(block["type"], "media_gallery")
                self.assertEqual(block["heading"], "Every day")
                self.assertEqual(len(block["items"]), 3)
                self.assertEqual(
                    [item["alt_text"] for item in block["items"]],
                    ["Day 1", "Day 2", "Day 3"],
                )

    def test_story_gallery_is_serialized_in_order(self):
        """Images picked in one pass keep the order they were arranged in."""
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                story = NewsEvent.objects.create(
                    content_type="news",
                    title="A story with a gallery",
                    slug="story-with-a-gallery",
                    excerpt="Photographs chosen in one pass.",
                )
                Image = get_image_model()
                for index in range(3):
                    NewsEventGalleryImage.objects.create(
                        story=story,
                        sort_order=index,
                        caption=f"Frame {index + 1}",
                        image=Image.objects.create(
                            title=f"Shot {index + 1}",
                            file=get_test_image_file(size=(1200, 800)),
                        ),
                    )

                payload = self.client.get(reverse("news-list")).json()["results"][0]
                gallery = payload["gallery"]
                self.assertEqual(len(gallery), 3)
                self.assertEqual(
                    [item["caption"] for item in gallery],
                    ["Frame 1", "Frame 2", "Frame 3"],
                )
                self.assertTrue(all(item["kind"] == "image" for item in gallery))
                self.assertNotIn("original_images", gallery[0]["thumb"])
                # The gallery also feeds the card slideshow.
                self.assertEqual(len(payload["card_media"]), 3)

    def test_body_can_position_the_story_gallery(self):
        """The placeholder renders the panel's images at that point."""
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                story = NewsEvent.objects.create(
                    content_type="news",
                    title="A story that places its gallery",
                    slug="story-that-places-its-gallery",
                    excerpt="Gallery sits mid-article.",
                    body=json.dumps(
                        [
                            {"type": "heading", "value": "Before"},
                            {
                                "type": "story_gallery",
                                "value": {"heading": "Day one", "caption": "Set."},
                            },
                            {"type": "heading", "value": "After"},
                        ]
                    ),
                )
                Image = get_image_model()
                for index in range(2):
                    NewsEventGalleryImage.objects.create(
                        story=story,
                        sort_order=index,
                        image=Image.objects.create(
                            title=f"Shot {index + 1}",
                            file=get_test_image_file(size=(900, 600)),
                        ),
                    )

                payload = self.client.get(reverse("news-list")).json()["results"][0]
                blocks = payload["body"]
                self.assertEqual(
                    [block["type"] for block in blocks],
                    ["heading", "media_gallery", "heading"],
                )
                self.assertEqual(blocks[1]["heading"], "Day one")
                self.assertEqual(len(blocks[1]["items"]), 2)
                # The page must not also render it at the end.
                self.assertTrue(payload["gallery_in_body"])
                self.assertEqual(len(payload["gallery"]), 2)

    def test_placeholder_without_gallery_images_is_dropped(self):
        NewsEvent.objects.create(
            content_type="news",
            title="A story with an unfilled gallery placeholder",
            slug="story-unfilled-gallery-placeholder",
            excerpt="Block added but no images chosen.",
            body=json.dumps(
                [
                    {"type": "story_gallery", "value": {"heading": "Gallery"}},
                    {"type": "heading", "value": "Still here"},
                ]
            ),
        )
        payload = self.client.get(reverse("news-list")).json()["results"][0]
        self.assertEqual([b["type"] for b in payload["body"]], ["heading"])
        # Nothing to place and nothing to append.
        self.assertTrue(payload["gallery_in_body"])
        self.assertEqual(payload["gallery"], [])

    def test_story_without_the_placeholder_reports_gallery_outside_body(self):
        NewsEvent.objects.create(
            content_type="news",
            title="A story with a trailing gallery",
            slug="story-with-trailing-gallery",
            excerpt="Gallery renders after the body.",
            body=json.dumps([{"type": "heading", "value": "Only text"}]),
        )
        payload = self.client.get(reverse("news-list")).json()["results"][0]
        self.assertFalse(payload["gallery_in_body"])

    def test_story_without_a_gallery_returns_an_empty_list(self):
        NewsEvent.objects.create(
            content_type="news",
            title="A story with no gallery",
            slug="story-with-no-gallery",
            excerpt="Text only.",
        )
        payload = self.client.get(reverse("news-list")).json()["results"][0]
        self.assertEqual(payload["gallery"], [])

    def test_event_end_date_is_exposed(self):
        start = timezone.now() + timedelta(days=10)
        NewsEvent.objects.create(
            content_type="event",
            title="Learning Express",
            slug="learning-express",
            excerpt="Runs over three days.",
            event_date=start,
            event_end_date=start + timedelta(days=2),
        )
        story = self.client.get(reverse("news-list")).json()["results"][0]
        self.assertIsNotNone(story["event_end_date"])
        self.assertGreater(story["event_end_date"], story["event_date"])

    def test_single_day_event_has_no_end_date(self):
        NewsEvent.objects.create(
            content_type="event",
            title="Open house",
            slug="open-house-single",
            excerpt="One day only.",
            event_date=timezone.now() + timedelta(days=5),
        )
        story = self.client.get(reverse("news-list")).json()["results"][0]
        self.assertIsNone(story["event_end_date"])


class SeedNewsEventsTests(TestCase):
    """The homepage news and events bands are fed by seeded starter entries."""

    def run_seed(self):
        """The targeted command, which is what the deployed backend can run."""
        call_command("seed_news_events", verbosity=0)

    def test_seed_creates_starter_news_and_events(self):
        self.run_seed()

        news = NewsEvent.objects.filter(content_type="news")
        events = NewsEvent.objects.filter(content_type="event")
        self.assertEqual(news.count(), 3)
        self.assertEqual(events.count(), 3)

        # Every seeded event must still be ahead of the seed run, otherwise the
        # homepage would open with a band of events that have already happened.
        now = timezone.now()
        for event in events:
            self.assertIsNotNone(event.event_date)
            self.assertGreater(event.event_date, now)

    def test_reseeding_keeps_author_edits(self):
        self.run_seed()

        entry = NewsEvent.objects.filter(content_type="news").first()
        entry.title = "Rewritten by an author in Wagtail"
        entry.save()

        self.run_seed()

        entry.refresh_from_db()
        self.assertEqual(entry.title, "Rewritten by an author in Wagtail")
        self.assertEqual(NewsEvent.objects.filter(content_type="news").count(), 3)


class SeedArticleBankTests(TestCase):
    """The drafted article bank, seeded without disturbing published work."""

    def run_seed(self):
        call_command("seed_article_bank", verbosity=0)

    def test_seed_creates_every_bank_article(self):
        self.run_seed()

        self.assertEqual(NewsEvent.objects.count(), len(ARTICLES))
        for entry in NewsEvent.objects.all():
            self.assertTrue(entry.excerpt)
            self.assertTrue(entry.category)
            self.assertEqual(len(entry.body), 3)

    def test_every_article_is_published(self):
        """The bank is publication-ready, so nothing is held back as a draft."""
        self.run_seed()

        self.assertEqual(
            NewsEvent.objects.filter(is_published=True).count(), len(ARTICLES)
        )
        self.assertFalse(NewsEvent.objects.filter(is_published=False).exists())

    def test_unapproved_personal_names_stay_out_of_the_body(self):
        """The document asks for these two names to be approved first, and a
        name published without consent cannot be taken back."""
        self.run_seed()

        for entry in NewsEvent.objects.all():
            self.assertNotIn("Liv Yi", str(entry.body))
            self.assertNotIn("Meas Sreypich", str(entry.body))

    def test_editorial_notes_never_reach_the_article_body(self):
        """`Suggested media` and `Publication check` are instructions to the
        author, not copy: they must not be published."""
        self.run_seed()

        for entry in NewsEvent.objects.all():
            body = str(entry.body)
            for phrase in ("Publication check", "Suggested media", "Card description"):
                self.assertNotIn(phrase, body, msg=f"{phrase} leaked into {entry.slug}")

    def test_existing_articles_are_left_untouched(self):
        """The four already on the site must survive a run unchanged."""
        live = NewsEvent.objects.create(
            sort_order=0,
            title="ME Lab Open House 2026",
            slug="staff-training-on-cnc-milling-machine",
            excerpt="Already written by an author.",
            body=[],
        )

        self.run_seed()

        live.refresh_from_db()
        self.assertEqual(live.title, "ME Lab Open House 2026")
        self.assertEqual(live.excerpt, "Already written by an author.")
        self.assertEqual(NewsEvent.objects.count(), len(ARTICLES))

    def test_reseeding_keeps_author_edits(self):
        self.run_seed()

        entry = NewsEvent.objects.get(slug="tuesday-weekly-seminar-technical-exchange")
        entry.title = "Rewritten in Wagtail"
        entry.save()

        self.run_seed()

        entry.refresh_from_db()
        self.assertEqual(entry.title, "Rewritten in Wagtail")
        self.assertEqual(NewsEvent.objects.count(), len(ARTICLES))
