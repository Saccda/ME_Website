from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import (
    CurriculumYearViewSet,
    FacilityViewSet,
    FacultyMemberViewSet,
    FocusAreaViewSet,
    InquiryCreateView,
    NewsEventViewSet,
    OpportunityViewSet,
    PartnerViewSet,
    ResearchProjectViewSet,
    health,
    home_data,
)

router = DefaultRouter()
router.register("focus-areas", FocusAreaViewSet, basename="focus-area")
router.register("curriculum", CurriculumYearViewSet, basename="curriculum")
router.register("research", ResearchProjectViewSet, basename="research")
router.register("partners", PartnerViewSet, basename="partner")
router.register("facilities", FacilityViewSet, basename="facility")
router.register("faculty", FacultyMemberViewSet, basename="faculty")
router.register("news", NewsEventViewSet, basename="news")
router.register("opportunities", OpportunityViewSet, basename="opportunity")

urlpatterns = [
    path("health/", health, name="health"),
    path("home/", home_data, name="home-data"),
    path("inquiries/", InquiryCreateView.as_view(), name="inquiry-create"),
    path("", include(router.urls)),
]
