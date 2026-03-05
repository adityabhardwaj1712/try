from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import NotificationViewSet, notifications_page


router = DefaultRouter()
router.register("api/notifications", NotificationViewSet, basename="notifications")

urlpatterns = [

    path("", notifications_page, name="notifications_page"),

]

urlpatterns += router.urls