from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from address.models import Address

EMPTY_BUILDING_NAME_ERROR = "Building Name should be input"
LONG_BUILDING_NAME_ERROR = "Building Name is too long"
EMPTY_STREET_NAME_ERROR = "Street Name should be input"
LONG_STREET_NAME_ERROR = "Street Name is too long"
EMPTY_BUILDING_NO_FROM_ERROR = "Building Number From should be input"
LONG_BUILDING_NO_FROM_ERROR = "Building Number From is too long"
EMPTY_BUILDING_NO_TO_ERROR = "Building Number To should be input"
LONG_BUILDING_NO_TO_ERROR = "Building Number To is too long"
EMPTY_DISTRICT_ERROR = "District should be input"
LONG_DISTRICT_ERROR = "District is too long"
EMPTY_FULL_ADDRESS_ERROR = "Full Address should be input"
LONG_FULL_ADDRESS_ERROR = "Full Address is too long"
EMPTY_RELATED_DOCUMENT_ERROR = "Related Document should be input"
LONG_RELATED_DOCUMENT_ERROR = "Related Document is too long"
EMPTY_UPLOAD_FILE_ERROR = "Upload File should be input"
LONG_UPLOAD_FILE_ERROR = "Upload File is too long"

class AddressForm(ModelForm):

    buildingName = forms.CharField(required=True, label='Building Name',
        error_messages={
            'required': EMPTY_BUILDING_NAME_ERROR,
            'max_length':LONG_BUILDING_NAME_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Building Name', 'autofocus': 'autofocus'}))
    streetName = forms.CharField(required=True, label='Street Name',
        error_messages={
            'required': EMPTY_STREET_NAME_ERROR,
            'max_length':LONG_STREET_NAME_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Street Name'}))
    buildingNoFrom = forms.CharField(required=True, label='Building No From',
        error_messages={
            'required': EMPTY_BUILDING_NO_FROM_ERROR,
            'max_length':LONG_BUILDING_NO_FROM_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Building No From'}))
    buildingNoTo = forms.CharField(required=True, label='Building No To',
        error_messages={
            'required': EMPTY_BUILDING_NO_TO_ERROR,
            'max_length':LONG_BUILDING_NO_TO_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Building No To'}))
    district = forms.CharField(required=True, label='Building No To',
        error_messages={
            'required': EMPTY_DISTRICT_ERROR,
            'max_length':LONG_DISTRICT_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'District'}))
    fullAddress = forms.CharField(required=True, label='District',
        error_messages={
            'required': EMPTY_FULL_ADDRESS_ERROR,
            'max_length':LONG_FULL_ADDRESS_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Full Address'}))
    relatedDocument = forms.CharField(required=True, label='Related Document',
        error_messages={
            'required': EMPTY_RELATED_DOCUMENT_ERROR,
            'max_length':LONG_RELATED_DOCUMENT_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Related Document'}))

    uploadFile = forms.FileField(required=False, label='Upload File',
        error_messages={
            'max_length':LONG_UPLOAD_FILE_ERROR},
        widget=forms.FileInput(attrs={'class': 'form-control','placeholder': 'Upload File'}))

    class Meta:
        model = Address
        fields = ['buildingName', 'streetName', 
            'buildingNoFrom', 'buildingNoFrom', 
            'buildingNoTo', 'district', 
            'fullAddress', 'relatedDocument', 'uploadFile']

