from django.core import mail
from datetime import timedelta

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from wagtail.models import Site

from .models import (
    Course,
    CurriculumYear,
    Facility,
    FocusArea,
    FocusAreaDetailItem,
    Inquiry,
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
