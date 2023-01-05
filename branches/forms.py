from django import forms
from .models import Branch
EMPTY_NAME_ERROR = "Name should be input"
LONG_NAME_ERROR = "Name is too long"
EMPTY_DESC_ERROR = "Description should be input"
LONG_DESC_ERROR = "Description is too long"
EMPTY_WKT_ERROR = "Geometry should be input"
LONG_WKT_ERROR = "Geometry is too long"

class BranchesForm(forms.Form):

    name = forms.CharField(required=True, label='Name', 
        max_length=Branch._meta.get_field('name').max_length,
        error_messages={
            'required': EMPTY_NAME_ERROR,
            'max_length':LONG_NAME_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Name', 'autofocus': 'autofocus'}))
    desc = forms.CharField(required=True, label='Description',
        error_messages={
            'required': EMPTY_DESC_ERROR,
            'max_length':LONG_DESC_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Description'}))   

    def clean(self):
        pass

class BranchesSpatialForm(BranchesForm):

    wkt = forms.CharField(required=True, label='Geometry',
        error_messages={
            'required': EMPTY_WKT_ERROR,
            'max_length':LONG_WKT_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Geometry'}))    
