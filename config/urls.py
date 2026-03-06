from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Models
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.organizations.models import Organization, Membership
from apps.users.models import User
from apps.activity.models import ActivityLog


# ==========================
# DASHBOARD VIEW
# ==========================

@login_required
def dashboard_view(request):

    # Organizations where the user is owner or member
    organizations = (
        Organization.objects.filter(owner=request.user) |
        Organization.objects.filter(memberships__user=request.user)
    ).distinct()

    # Projects in those organizations
    projects = Project.objects.filter(
        organization__in=organizations
    )

    # Tasks in those organizations
    tasks = Task.objects.filter(
        organization__in=organizations
    )

    # Users in those organizations
    users = User.objects.filter(
        memberships__organization__in=organizations
    ).distinct()

    # Stats
    projects_count = projects.count()
    tasks_count = tasks.count()
    completed_tasks = tasks.filter(status="DONE").count()
    members_count = users.count()

    # Recent activity
    activity_logs = ActivityLog.objects.filter(
        organization__in=organizations
    ).select_related(
        "user", "organization"
    ).order_by("-created_at")[:10]

    context = {
        "organizations": organizations,
        "projects": projects,
        "users": users,
        "projects_count": projects_count,
        "tasks_count": tasks_count,
        "completed_tasks": completed_tasks,
        "members_count": members_count,
        "activity_logs": activity_logs,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


# ==========================
# URL PATTERNS
# ==========================

urlpatterns = [

    # Admin
    path("admin/", admin.site.urls),

    # -------------------------
    # JWT AUTH API
    # -------------------------

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # -------------------------
    # Dashboard
    # -------------------------

    path("", dashboard_view, name="dashboard"),

    # -------------------------
    # Authentication
    # -------------------------

    path("", include("apps.users.urls")),

    # -------------------------
    # UI Routes
    # -------------------------

    path("organizations/", include("apps.organizations.urls")),
    path("projects/", include("apps.projects.urls")),
    path("tasks/", include("apps.tasks.urls")),
    path("comments/", include("apps.comments.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("activity/", include("apps.activity.urls")),

    # -------------------------
    # API Routes
    # -------------------------

    path("api/projects/", include("apps.projects.urls")),
    path("api/tasks/", include("apps.tasks.urls")),
    path("api/comments/", include("apps.comments.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/organizations/", include("apps.organizations.urls")),
    path("api/activity/", include("apps.activity.urls")),
]