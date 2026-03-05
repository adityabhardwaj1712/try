from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("action", "organization", "user", "created_at")
    search_fields = ("action",)