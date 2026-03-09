from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.task_board,
        name="task_board"
    ),

    path(
        "create/",
        views.create_task,
        name="create_task"
    ),

    path(
        "update-status/<int:task_id>/",
        views.update_task_status,
        name="update_task_status"
    ),

]