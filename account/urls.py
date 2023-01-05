
from django.urls import path

from . import views
from .views import (
        TokenView,
    )

app_name = 'account'

urlpatterns = [
    path("", views.index, name="index"),
    path("token", TokenView.as_view(), name="token"),
    path("profile_update", views.profile_update, name="profile_update"),
    path("delete_device", views.delete_device, name="delete_device"),

]