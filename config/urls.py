from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.projects.models import Project
from apps.tasks.models import Task
from apps.organizations.models import Membership
from apps.activity.models import ActivityLog


@login_required
def dashboard_view(request):

    projects_count = Project.objects.count()
    tasks_count = Task.objects.count()
    completed_tasks = Task.objects.filter(status="DONE").count()
    members_count = Membership.objects.count()

    activity_logs = ActivityLog.objects.all()[:10]

    context = {
        "projects_count": projects_count,
        "tasks_count": tasks_count,
        "completed_tasks": completed_tasks,
        "members_count": members_count,
        "activity_logs": activity_logs,
    }

    return render(request, "dashboard/dashboard.html", context)


urlpatterns = [

    path("admin/", admin.site.urls),

    # dashboard
    path("", dashboard_view, name="dashboard"),

    # auth + users
    path("", include("apps.users.urls")),

    # UI routes
    path("projects/", include("apps.projects.urls")),
    path("tasks/", include("apps.tasks.urls")),
    path("comments/", include("apps.comments.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("organizations/", include("apps.organizations.urls")),

    # API routes
    path("api/projects/", include("apps.projects.urls")),
    path("api/tasks/", include("apps.tasks.urls")),
    path("api/comments/", include("apps.comments.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/organizations/", include("apps.organizations.urls")),
]