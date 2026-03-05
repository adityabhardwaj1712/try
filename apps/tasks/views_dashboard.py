from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def task_list_page(request):
    return render(request, "dashboard/task_list.html")