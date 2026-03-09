from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    NotificationViewSet,
    notifications_page,
    mark_notification_read
)

# DRF Router
router = DefaultRouter()
router.register(
    "api/notifications",
    NotificationViewSet,
    basename="notifications"
)

urlpatterns = [

    # dashboard notifications page
    path(
        "",
        notifications_page,
        name="notifications_page"
    ),

    # mark notification as read
    path(
        "read/<int:pk>/",
        mark_notification_read,
        name="mark_notification_read"
    ),

]

# include API routes
urlpatterns += router.urls