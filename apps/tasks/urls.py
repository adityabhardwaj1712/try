from django.urls import path
from . import views

urlpatterns = [

    # Task board
    path(
        "",
        views.task_board,
        name="task_board"
    ),

    # Create task
    path(
        "create/",
        views.create_task,
        name="create_task"
    ),

    # Update status
    path(
        "update-status/<int:task_id>/",
        views.update_task_status,
        name="update_task_status"
    ),

]