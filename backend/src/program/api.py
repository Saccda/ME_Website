from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Prefetch, Q
from django.utils import timezone
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import (
    Course,
    CurriculumYear,
    Facility,
    FacultyMember,
    FocusArea,
    Inquiry,
    NewsEvent,
    Opportunity,
    Partner,
    ProgramSettings,
    ResearchProject,
    WhyChooseItem,
)
from .serializers import (
    CurriculumYearSerializer,
    FacilitySerializer,
    FacultyMemberSerializer,
    FocusAreaDetailSerializer,
    FocusAreaSerializer,
    InquirySerializer,
    NewsEventSerializer,
    OpportunitySerializer,
    PartnerSerializer,
    ProgramSettingsSerializer,
    ResearchProjectSerializer,
    WhyChooseItemSerializer,
)


class PublicReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)


class FocusAreaViewSet(PublicReadOnlyViewSet):
    serializer_class = FocusAreaSerializer
    lookup_field = "slug"
    search_fields = ("code", "title", "description")
    ordering_fields = ("sort_order", "code", "title")

    def get_queryset(self):
        return (
            FocusArea.objects.select_related("image")
            .prefetch_related(
                "detail_items",
                "facilities__image",
                "courses__curriculum_year",
                "research_projects__image",
                "research_projects__focus_areas",
                "research_projects__focus_areas__image",
                "research_projects__focus_areas__detail_items",
            )
            .all()
        )

    def get_serializer_class(self):
        return (
            FocusAreaDetailSerializer
            if self.action == "retrieve"
            else FocusAreaSerializer
        )


class CurriculumYearViewSet(PublicReadOnlyViewSet):
    queryset = CurriculumYear.objects.prefetch_related(
        Prefetch("courses", queryset=Course.objects.order_by("sort_order", "code"))
    )
    serializer_class = CurriculumYearSerializer
    lookup_field = "year"
    ordering_fields = ("year", "sort_order")


class ResearchProjectViewSet(PublicReadOnlyViewSet):
    serializer_class = ResearchProjectSerializer
    lookup_field = "slug"
    search_fields = ("title", "summary", "body", "focus_areas__code")
    ordering_fields = ("sort_order", "published_at", "title")

    def get_queryset(self):
        queryset = (
            ResearchProject.objects.filter(is_published=True)
            .select_related("image")
            .prefetch_related("focus_areas", "focus_areas__image", "focus_areas__detail_items")
            .order_by("sort_order", "-published_at")
        )
        focus = self.request.query_params.get("focus")
        if focus:
            queryset = queryset.filter(focus_areas__code__iexact=focus)
        return queryset.distinct()


class PartnerViewSet(PublicReadOnlyViewSet):
    queryset = Partner.objects.select_related("logo").all()
    serializer_class = PartnerSerializer
    search_fields = ("name", "partner_type")
    ordering_fields = ("sort_order", "name", "partner_type")


def active_opportunities():
    today = timezone.localdate()
    return (
        Opportunity.objects.filter(
            is_published=True,
            published_at__lte=timezone.now(),
        )
        .filter(
            Q(application_deadline__isnull=True)
            | Q(application_deadline__gte=today)
        )
        .select_related("partner", "partner__logo", "announcement_image")
        .prefetch_related("focus_areas")
        .order_by("-is_featured", "sort_order", "application_deadline", "-published_at")
    )


class OpportunityViewSet(PublicReadOnlyViewSet):
    serializer_class = OpportunitySerializer
    lookup_field = "slug"
    search_fields = (
        "title",
        "summary",
        "location",
        "partner__name",
        "focus_areas__code",
    )
    ordering_fields = (
        "sort_order",
        "application_deadline",
        "published_at",
        "title",
    )

    def get_queryset(self):
        queryset = active_opportunities()
        focus = self.request.query_params.get("focus")
        opportunity_type = self.request.query_params.get("type")
        if focus:
            queryset = queryset.filter(focus_areas__code__iexact=focus)
        if opportunity_type:
            queryset = queryset.filter(opportunity_type=opportunity_type)
        return queryset.distinct()


class FacultyMemberViewSet(PublicReadOnlyViewSet):
    queryset = (
        FacultyMember.objects.filter(is_published=True)
        .select_related("photo")
        .prefetch_related(
            "focus_areas",
            "focus_areas__image",
            "work_items",
            "work_items__image",
        )
    )
    serializer_class = FacultyMemberSerializer
    search_fields = ("name", "role", "bio", "focus_areas__code")
    ordering_fields = ("sort_order", "name")


class FacilityViewSet(PublicReadOnlyViewSet):
    queryset = Facility.objects.select_related("image").all()
    serializer_class = FacilitySerializer
    search_fields = ("name", "description")
    ordering_fields = ("sort_order", "name")


class NewsEventViewSet(PublicReadOnlyViewSet):
    serializer_class = NewsEventSerializer
    lookup_field = "slug"
    search_fields = ("title", "excerpt", "body")
    ordering_fields = ("published_at", "event_date", "sort_order")

    def get_queryset(self):
        queryset = (
            NewsEvent.objects.filter(is_published=True, published_at__lte=timezone.now())
            .select_related("image")
            .prefetch_related("gallery_images__image")
            .order_by("-published_at", "sort_order")
        )
        content_type = self.request.query_params.get("type")
        return queryset.filter(content_type=content_type) if content_type else queryset


class InquiryCreateView(generics.CreateAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = (AllowAny,)
    throttle_scope = "inquiries"

    def perform_create(self, serializer):
        inquiry = serializer.save()
        send_mail(
            subject=f"[ME Website] {inquiry.get_inquiry_type_display()}: {inquiry.subject}",
            message=(
                f"Name: {inquiry.name}\n"
                f"Email: {inquiry.email}\n"
                f"Phone: {inquiry.phone}\n"
                f"Organization: {inquiry.organization}\n\n"
                f"{inquiry.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
            fail_silently=True,
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "message": "Thank you. Your enquiry has been received.",
                "id": response.data["id"],
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response({"status": "ok", "service": "ME RUPP API"})


@api_view(["GET"])
@permission_classes([AllowAny])
def home_data(request):
    program_settings = ProgramSettings.objects.select_related("hero_image").first()
    context = {"request": request}
    return Response(
        {
            "settings": (
                ProgramSettingsSerializer(program_settings, context=context).data
                if program_settings
                else None
            ),
            "why_choose": WhyChooseItemSerializer(
                WhyChooseItem.objects.select_related("image").all(),
                many=True,
                context=context,
            ).data,
            "focus_areas": FocusAreaSerializer(
                FocusArea.objects.select_related("image").prefetch_related(
                    "detail_items"
                ),
                many=True,
                context=context,
            ).data,
            "curriculum": CurriculumYearSerializer(
                CurriculumYear.objects.prefetch_related("courses").all(),
                many=True,
                context=context,
            ).data,
            "research": ResearchProjectSerializer(
                ResearchProject.objects.filter(is_published=True)
                .select_related("image")
                .prefetch_related(
                    "focus_areas",
                    "focus_areas__image",
                    "focus_areas__detail_items",
                )
                .order_by("sort_order", "-published_at")[:8],
                many=True,
                context=context,
            ).data,
            "partners": PartnerSerializer(
                Partner.objects.select_related("logo").all(),
                many=True,
                context=context,
            ).data,
            "opportunities": OpportunitySerializer(
                active_opportunities()[:10],
                many=True,
                context=context,
            ).data,
            "facilities": FacilitySerializer(
                Facility.objects.filter(is_featured=True).select_related("image"),
                many=True,
                context=context,
            ).data,
        }
    )
