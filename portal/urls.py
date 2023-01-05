from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("no-permission", views.no_permission, name="no-permission"),
    path("error", views.error, name="error"),
    path("readme", views.readme_view, name="readme"),
]
