from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


def health_check(request):
    return JsonResponse({"status": "ok"})


@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")


urlpatterns = [

    # Health
    path("health/", health_check, name="health"),

    # Admin (optional)
    path("admin/", admin.site.urls),

    # -----------------------------
    # AUTH (Frontend Session Login)
    # -----------------------------

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),

    # -----------------------------
    # DASHBOARD (Main Frontend Page)
    # -----------------------------

    path("", dashboard_view, name="dashboard"),

    # -----------------------------
    # JWT (API Authentication)
    # -----------------------------

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # -----------------------------
    # API Routes
    # -----------------------------

    path("api/users/", include("apps.users.urls")),
    path("api/organizations/", include("apps.organizations.urls")),
    path("api/projects/", include("apps.projects.urls")),
    path("api/tasks/", include("apps.tasks.urls")),
    path("api/comments/", include("apps.comments.urls")),
    path("api/activity/", include("apps.activity.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
]