from django.urls import path
from .views import project_list, create_project, project_detail

urlpatterns = [

    path("", project_list, name="project_list"),

    path("create/", create_project, name="create_project"),

    path("<int:pk>/", project_detail, name="project_detail"),

]