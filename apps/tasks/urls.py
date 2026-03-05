from django.urls import path
from .views import task_board

urlpatterns = [

    path("", task_board, name="task_board"),

]