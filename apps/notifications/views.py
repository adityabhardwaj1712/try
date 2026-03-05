from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Notification
from .serializers import NotificationSerializer

from apps.users.models import User
from apps.projects.models import Project


# ==============================
# API VIEWSET (DRF API)
# ==============================

class NotificationViewSet(viewsets.ModelViewSet):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        if self.request.user.role not in ["ADMIN", "MANAGER"]:
            raise PermissionDenied("You cannot send notifications")

        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):

        notification = self.get_object()

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return Response({"status": "marked as read"})


# ==============================
# DASHBOARD PAGE VIEW
# ==============================
@login_required
def notifications_page(request):

    users = User.objects.all()
    projects = Project.objects.select_related("organization")

    if request.method == "POST":

        message = request.POST.get("message")
        user_id = request.POST.get("user")

        Notification.objects.create(
            message=message,
            user_id=user_id,
        )

        return redirect("notifications_page")

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "dashboard/notifications.html",
        {
            "notifications": notifications,
            "users": users,
            "projects": projects
        }
    )