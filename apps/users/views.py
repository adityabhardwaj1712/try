from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import CreateUserForm

User = get_user_model()


# --------------------
# LOGIN VIEW
# --------------------
def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")

        return render(request, "login.html", {
            "error": "Invalid credentials"
        })

    return render(request, "login.html")


# --------------------
# LOGOUT VIEW
# --------------------
def logout_view(request):

    logout(request)

    return redirect("/login/")


# --------------------
# USERS PAGE
# --------------------
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