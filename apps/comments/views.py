from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from apps.tasks.models import Task
from apps.organizations.models import Membership
from .models import Comment


@login_required
def comments_page(request):

    tasks = Task.objects.filter(
        project__organization__memberships__user=request.user
    ).select_related("project")

    if request.method == "POST":

        content = request.POST.get("content")
        task_id = request.POST.get("task")

        task = get_object_or_404(Task, id=task_id)

        membership = Membership.objects.filter(
            user=request.user,
            organization=task.organization
        ).first()

        if not membership:
            return HttpResponseForbidden("Permission denied")

        if content:

            Comment.objects.create(
                content=content,
                task=task,
                user=request.user
            )

            return redirect("/comments/")

    comments = Comment.objects.filter(
        task__organization__memberships__user=request.user
    ).select_related(
        "task", "user"
    ).order_by("-created_at")

    return render(
        request,
        "dashboard/comments.html",
        {
            "comments": comments,
            "tasks": tasks
        }
    )