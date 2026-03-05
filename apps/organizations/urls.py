from django.urls import path
from .views import organization_list, create_organization, organization_detail

urlpatterns = [

    path("", organization_list, name="organization_list"),

    path("create/", create_organization, name="create_organization"),

    path("<int:pk>/", organization_detail, name="organization_detail"),

]