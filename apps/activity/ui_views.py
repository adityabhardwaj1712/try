from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def activity_page(request):

    return render(
        request,
        "dashboard/activity.html"
    )