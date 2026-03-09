from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Notification
from .serializers import NotificationSerializer

from apps.users.models import User
from apps.projects.models import Project

class NotificationViewSet(viewsets.ModelViewSet):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Notification.objects.select_related(
            "sender",
            "project",
            "project__organization"
        ).filter(
            Q(user=self.request.user) | Q(sender=self.request.user)
        ).order_by("-created_at")

    def perform_create(self, serializer):

        if self.request.user.role not in ["ADMIN", "MANAGER"]:
            raise PermissionDenied("You cannot send notifications")

        notification = serializer.save(sender=self.request.user)

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"user_{notification.user.id}",
            {
                "type": "send_notification",
                "message": notification.message
            }
        )

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):

        notification = self.get_object()

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return Response({"status": "marked as read"})

@login_required
def notifications_page(request):

    users = User.objects.exclude(id=request.user.id)

    projects = Project.objects.select_related("organization")

    if request.method == "POST":

        message = request.POST.get("message")
        user_id = request.POST.get("user")
        project_id = request.POST.get("project")

        notification = Notification.objects.create(
            message=message,
            user_id=user_id,
            sender=request.user,
            project_id=project_id if project_id else None,
            notification_type="GENERAL"
        )

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "send_notification",
                "message": message
            }
        )

        return redirect("notifications_page")

    notifications = Notification.objects.select_related(
        "sender",
        "project",
        "project__organization"
    ).filter(
        Q(user=request.user) | Q(sender=request.user)
    ).order_by("-created_at")

    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)

    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return render(
        request,
        "dashboard/notifications.html",
        {
            "notifications": notifications,
            "users": users,
            "projects": projects,
            "unread_count": unread_count
        }
    )

@login_required
def mark_notification_read(request, pk):

    notification = get_object_or_404(Notification, pk=pk)

    notification.is_read = True
    notification.save(update_fields=["is_read"])

    return redirect("notifications_page")