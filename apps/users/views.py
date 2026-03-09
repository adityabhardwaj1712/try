from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import CreateUserForm
from apps.organizations.models import Membership

User = get_user_model()


def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:

            login(request, user)

            next_url = request.GET.get("next")

            return redirect(next_url or "/")

        return render(
            request,
            "login.html",
            {"error": "Invalid credentials"}
        )

    return render(request, "login.html")


def logout_view(request):

    logout(request)

    return redirect("/login/")


@login_required
def users_page(request):

    users = User.objects.all()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            role = form.cleaned_data["role"]
            organization = form.cleaned_data["organization"]

            if request.user.role == "VIEWER":
                return render(
                    request,
                    "dashboard/no_permission.html"
                )

            if request.user.role == "MANAGER" and role != "VIEWER":
                return render(
                    request,
                    "dashboard/no_permission.html"
                )

            user = form.save(commit=False)

            user.set_password(form.cleaned_data["password"])

            user.save()

            Membership.objects.create(
                user=user,
                organization=organization,
                role=role
            )

            return redirect("/users/")

    else:

        form = CreateUserForm()

    return render(
        request,
        "dashboard/users.html",
        {
            "users": users,
            "form": form
        }
    )