from django.urls import path
from .views import task_board, create_task

urlpatterns = [

    path("", task_board, name="task_board"),

    path("create/", create_task, name="create_task"),

]