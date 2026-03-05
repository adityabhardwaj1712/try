from django.urls import path
from .views import login_view, logout_view, users_page

urlpatterns = [

    path("login/", login_view, name="login"),

    path("logout/", logout_view, name="logout"),

    path("users/", users_page, name="users"),

]