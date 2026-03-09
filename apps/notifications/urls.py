from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    NotificationViewSet,
    notifications_page,
    mark_notification_read
)

router = DefaultRouter()
router.register(
    "api/notifications",
    NotificationViewSet,
    basename="notifications"
)

urlpatterns = [

    path(
        "",
        notifications_page,
        name="notifications_page"
    ),

    path(
        "read/<int:pk>/",
        mark_notification_read,
        name="mark_notification_read"
    ),

]

urlpatterns += router.urls