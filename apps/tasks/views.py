from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Task
from projects.models import Project


@login_required
def task_board(request):

    tasks = Task.objects.filter(
        assignee=request.user
    )

    todo_tasks = tasks.filter(status="TODO")
    progress_tasks = tasks.filter(status="IN_PROGRESS")
    done_tasks = tasks.filter(status="DONE")

    context = {
        "todo_tasks": todo_tasks,
        "progress_tasks": progress_tasks,
        "done_tasks": done_tasks,
    }

    return render(request, "dashboard/task_board.html", context)


@login_required
def create_task(request, project_id):

    if not request.user.can_manage():
        return HttpResponseForbidden("Permission denied")

    project = Project.objects.get(id=project_id)

    if request.method == "POST":

        Task.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            project=project,
            organization=project.organization,
            created_by=request.user
        )

        return redirect("/tasks/")

    return render(request, "dashboard/create_task.html")