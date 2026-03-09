from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Task
from apps.projects.models import Project
from apps.users.models import User
from apps.organizations.models import Membership
from apps.notifications.models import Notification

@login_required
def task_board(request):

    tasks = Task.objects.filter(
        project__organization__memberships__user=request.user
    ).select_related(
        "project",
        "assignee"
    ).distinct()

    todo_tasks = tasks.filter(status="TODO")
    progress_tasks = tasks.filter(status="IN_PROGRESS")
    done_tasks = tasks.filter(status="DONE")

    projects = Project.objects.filter(
        organization__memberships__user=request.user
    ).distinct()

    memberships = Membership.objects.filter(user=request.user)

    users = User.objects.filter(
        memberships__organization__in=memberships.values_list(
            "organization", flat=True
        )
    ).exclude(
        id=request.user.id
    ).distinct()

    context = {
        "tasks": tasks,
        "todo_tasks": todo_tasks,
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


@login_required
def create_task(request):

    projects = Project.objects.filter(
        organization__memberships__user=request.user
    ).select_related("organization")

    memberships = Membership.objects.filter(user=request.user)

    users = User.objects.filter(
        memberships__organization__in=memberships.values_list(
            "organization", flat=True
        )
    ).exclude(
        id=request.user.id
    ).distinct()

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        project_id = request.POST.get("project")
        assignee_id = request.POST.get("assignee")

        if not project_id:
            return render(
                request,
                "dashboard/create_task.html",
                {
                    "projects": projects,
                    "users": users,
                    "error": "Project is required"
                }
            )

        project = get_object_or_404(Project, id=project_id)

        membership = Membership.objects.filter(
            user=request.user,
            organization=project.organization
        ).first()

        if not membership:
            return HttpResponseForbidden("Not part of this organization")

        if membership.role == "VIEWER":
            return render(request, "dashboard/no_permission.html")

        assignee = None

        if assignee_id:
            assignee = User.objects.filter(id=assignee_id).first()

        task = Task.objects.create(
            title=title,
            description=description,
            project=project,
            organization=project.organization,
            assignee=assignee,
            created_by=request.user,
            status="TODO"
        )

        if assignee:
            Notification.objects.create(
                user=assignee,
                sender=request.user,
                project=project,
                message=f"{request.user.email} assigned you a task: {task.title}"
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


@login_required
def update_task_status(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    membership = Membership.objects.filter(
        user=request.user,
        organization=task.organization
    ).first()

    if not membership:
        return HttpResponseForbidden("Not part of this organization")

    if request.method == "POST":

        status = request.POST.get("status")

        if status in ["TODO", "IN_PROGRESS", "DONE"]:
            task.status = status
            task.save()

    return redirect("task_board")