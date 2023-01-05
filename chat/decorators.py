from functools import wraps
import json as simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from chat.models import Membership

def chat_room_access_right_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        room_name = kwargs.get('room_name')
        obj = Membership.objects.filter(chat_room__name=room_name, user=request.user).first()
        if request.user.is_authenticated and obj != None :
            return view_func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('no-permission'))
    return wrapper