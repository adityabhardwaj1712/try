from django.urls import path
from .views import comments_page

urlpatterns = [
    path("", comments_page, name="comments_page"),
]