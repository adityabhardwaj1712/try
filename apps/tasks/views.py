from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Task
from apps.projects.models import Project
from apps.users.models import User


# =============================
# TASK BOARD
# =============================

@login_required
def task_board(request):

    tasks = Task.objects.filter(
        project__organization__memberships__user=request.user
    ).select_related("project", "assignee")

    todo_tasks = tasks.filter(status="TODO")
    progress_tasks = tasks.filter(status="IN_PROGRESS")
    done_tasks = tasks.filter(status="DONE")

    context = {
        "todo_tasks": todo_tasks,
        "progress_tasks": progress_tasks,
        "done_tasks": done_tasks,
    }

    return render(
        request,
        "dashboard/task_board.html",
        context
    )


# =============================
# CREATE TASK
# =============================

@login_required
def create_task(request):

    if request.user.role not in ["ADMIN", "MANAGER"] and not request.user.is_superuser:
        return HttpResponseForbidden("Permission denied")

    projects = Project.objects.select_related("organization")
    users = User.objects.all()

    if request.method == "POST":

        project_id = request.POST.get("project")
        project = get_object_or_404(Project, id=project_id)

        Task.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            project=project,
            organization=project.organization,
            assignee_id=request.POST.get("assignee"),
            created_by=request.user
        )

        return redirect("task_board")

    return render(
        request,
        "dashboard/create_task.html",
        {
            "projects": projects,
            "users": users
        }
    )