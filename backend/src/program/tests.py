import json
import tempfile
from datetime import timedelta

from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from wagtail.images import get_image_model
from wagtail.images.tests.utils import get_test_image_file
from wagtail.models import Site

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
