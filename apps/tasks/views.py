from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Task
from apps.projects.models import Project
from apps.users.models import User
from apps.organizations.models import Membership


# =============================
# TASK BOARD
# =============================

@login_required
def task_board(request):

    # All tasks user can see
    tasks = Task.objects.filter(
        project__organization__memberships__user=request.user
    ).select_related(
        "project",
        "assignee"
    ).distinct()

    # Kanban columns
    todo_tasks = tasks.filter(status="TODO")
    progress_tasks = tasks.filter(status="IN_PROGRESS")
    done_tasks = tasks.filter(status="DONE")

    # Projects user belongs to
    projects = Project.objects.filter(
        organization__memberships__user=request.user
    ).distinct()

    # Organizations where user belongs
    memberships = Membership.objects.filter(
        user=request.user
    )

    # Users in those organizations
    users = User.objects.filter(
        memberships__organization__in=memberships.values_list(
            "organization", flat=True
        )
    ).distinct()

    context = {
        "tasks": tasks,                 # ⭐ Needed for table view
        "todo_tasks": todo_tasks,       # Kanban TODO
        "progress_tasks": progress_tasks,
        "done_tasks": done_tasks,
        "projects": projects,
        "users": users,
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

    projects = Project.objects.filter(
        organization__memberships__user=request.user
    ).select_related("organization")

    memberships = Membership.objects.filter(
        user=request.user
    )

    users = User.objects.filter(
        memberships__organization__in=memberships.values_list(
            "organization", flat=True
        )
    ).distinct()

    if request.method == "POST":

        project_id = request.POST.get("project")
        project = get_object_or_404(Project, id=project_id)

        membership = Membership.objects.filter(
            user=request.user,
            organization=project.organization
        ).first()

        if not membership:
            return HttpResponseForbidden("Not part of this organization")

        # Viewer cannot create task
        if membership.role == "VIEWER":
            return render(
                request,
                "dashboard/no_permission.html"
            )

        Task.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            project=project,
            organization=project.organization,
            assignee_id=request.POST.get("assignee"),
            created_by=request.user,
            status="TODO"
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


# =============================
# UPDATE TASK STATUS
# =============================

@login_required
def update_task_status(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    membership = Membership.objects.filter(
        user=request.user,
        organization=task.organization
    ).first()

    if not membership:
        return HttpResponseForbidden("Not part of this organization")

    # Any member can update status
    if request.method == "POST":

        status = request.POST.get("status")

        if status in ["TODO", "IN_PROGRESS", "DONE"]:
            task.status = status
            task.save()

    return redirect("task_board")