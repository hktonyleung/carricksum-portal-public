from functools import wraps
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django_otp import user_has_device

def otp2_required_with_title(title):
    def otp2_required(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_verified():
                return view_func(request, *args, **kwargs)
            elif not user_has_device(request.user):
                return HttpResponseRedirect(reverse('account:index'))
            return HttpResponseRedirect(reverse('account:token', args=(), kwargs={})+'?title=' + title +'&next='+request.path)
        return wrapper
    return otp2_required
