from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class ProfileForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

class TokenForm(forms.Form):
    token = forms.CharField(required=True)
    next = forms.CharField(required=False)
