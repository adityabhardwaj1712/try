from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def users_page(request):

    users = User.objects.all()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            return redirect("/users/")

    else:
        form = CreateUserForm()

    return render(request, "dashboard/users.html", {
        "users": users,
        "form": form
    })