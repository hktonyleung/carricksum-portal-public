from django.shortcuts import render,reverse
from django.views.generic.detail import View
from django.views.generic.edit import CreateView
from django_otp import devices_for_user, login, user_has_device
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.forms import OTPTokenForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from functools import partial
from portal.utils import generate_qrcode
from .forms import ProfileForm, TokenForm
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django_otp.decorators import otp_required
from .decorators import otp2_required_with_title

@login_required
def profile_update(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
    else:
        form = ProfileForm()
    return save_profile_form(request, form, 'account/partial_profile_update.html')

def save_profile_form(request, form, template_name):
    user = request.user
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name'] 
            user.last_name = form.cleaned_data['last_name']
            user.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def index(request):
    if request.method == "GET":
        context = check_user_totp_device(request.user)
        return render(request, "account/index.html", context)

def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


def check_user_totp_device(user):
    context = {}
    if user_has_device(user, confirmed=True):
        context['has_device'] = True
        context['confirmed'] = True
    elif user_has_device(user, confirmed=False):
        context['has_device'] = True
        context['confirmed'] = False
    else:
        context['has_device'] = False
        context['confirmed'] = False  

    return context  

@otp_required()
def delete_device(request):
    user = request.user
    user.totpdevice_set.all().delete()
    return HttpResponseRedirect(reverse('account:index'))

class TokenView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {}
        #context['title'] = title
        device = get_user_totp_device(self, user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
            url = device.config_url
            context['svg'] = generate_qrcode(url, 10)
        return render(request, "account/token_form.html", context)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        form = TokenForm(request.POST)
        context = {}
        if form.is_valid():
            token = form.cleaned_data['token']
            next = form.cleaned_data['next']
            device = get_user_totp_device(self, user)
            if not device == None and device.verify_token(token):
                '''
                1. For device confirmation
                2. For login and redirect page
                '''
                if device.confirmed == False:
                    device.confirmed = True
                    device.save()
                
                if next == "":
                    return HttpResponseRedirect(reverse('account:index'))
                else:
                    login(request, device)
                    return HttpResponseRedirect(next)
            else:
                context['2fa_success'] = False
                next = form.cleaned_data['next']
                context['err'] = "Token value is incorrect"
                context['form'] = form
                context['next'] = next
                return render(request, "account/token_form.html", context)
        else:
            next = form.cleaned_data['next']
            context['form'] = form
            context['next'] = next
            return render(request, "account/token_form.html", context)
