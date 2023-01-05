from this import d
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Announcement
from portal.utils import get_readme

#import markdown2 as md

@login_required
def index(request):
    announcements = Announcement.objects.get_active_announcement()
    announcement_count = announcements.count()
    context = {'announcements':announcements, 'announcement_count':announcement_count}
    return render(request, "portal/index.html", context)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)

            nxt = request.POST["next"]
            if nxt is None or not nxt.strip():
                return HttpResponseRedirect(reverse("index"))
            else: 
                return redirect(nxt)
        else:
            return render(request, "portal/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "portal/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "portal/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "portal/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "portal/register.html")

def no_permission(request):
    return render(request, "portal/no_permission.html")

def error(request, context):
    return render(request, "portal/error.html", context)

# TODO
def readme_view(request):
    # html_entry = md.markdown(get_readme())
    html_entry = None
    return render(request, "portal/readme.html", {
            "entry": html_entry
    })
