from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.tasks.models import Task
from .models import Comment


@login_required
def comments_page(request):

    tasks = Task.objects.select_related("project")

    if request.method == "POST":

        content = request.POST.get("content")
        task_id = request.POST.get("task")

        if content and task_id:

            Comment.objects.create(
                content=content,
                task_id=task_id,
                user=request.user
            )

            return redirect("/comments/")

    comments = Comment.objects.select_related(
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