from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def comments_page(request):

    return render(
        request,
        "dashboard/comments.html"
    )