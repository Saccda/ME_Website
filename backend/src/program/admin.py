from django.contrib import admin

from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "inquiry_type", "subject", "status", "created_at")
    list_filter = ("inquiry_type", "status", "created_at")
    search_fields = ("name", "email", "organization", "subject", "message")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
