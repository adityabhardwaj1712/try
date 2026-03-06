from django.urls import path
from .views import task_board, create_task, update_task_status

urlpatterns = [
    path("", task_board, name="task_board"),
    path("create/", create_task, name="create_task"),
    path("update-status/<int:task_id>/", update_task_status, name="update_task_status"),
]