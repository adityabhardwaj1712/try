from django.urls import path
from .views import organization_list, organization_detail

urlpatterns = [

    path("", organization_list, name="organization_list"),

    path("<int:pk>/", organization_detail, name="organization_detail"),

]