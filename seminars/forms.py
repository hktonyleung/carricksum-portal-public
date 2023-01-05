from django import forms
from django.forms import ModelForm
from seminars.models import Room, Seminar
from django.core.exceptions import ValidationError

EMPTY_NO_ERROR = "No should be input"
LONG_NO_ERROR = "No is too long"
EMPTY_DESC_ERROR = "Description should be input"
LONG_DESC_ERROR = "Description is too long"

EMPTY_TOPIC_ERROR = "Topic should be input"
EMPTY_START_DATE_TIME_ERROR = "Start Date Time should be input"
EMPTY_END_DATE_TIME_ERROR = "End Date Time should be input"

LONG_TOPIC_ERROR = "Topic is too long"
INVALID_NO_OF_AVAILABLE_SEAT_ERROR = "Number of available seat should be larger than 0"
INVALID_SEMINAR_DATE_RANGE_ERROR = "Conflict found on same venue and date time range"
INVALID_SEMINAR_START_END_DATETIME_ERROR = "End Date Time should be after Start Date Time"
SEMINAR_FULL_ERROR="No more seat available"

class RoomForm(ModelForm):

    no = forms.CharField(required=True, label='Number',
        error_messages={
            'required': EMPTY_NO_ERROR,
            'max_length':LONG_NO_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Number', 'autofocus': 'autofocus'}))
    desc = forms.CharField(required=True, label='Description',
        error_messages={
            'required': EMPTY_DESC_ERROR,
            'max_length':LONG_DESC_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Description'}))

    class Meta:
        model = Room
        fields = ['no', 'desc']

class SeminarForm(ModelForm):

    topic = forms.CharField(required=True,
            error_messages={
            'required': EMPTY_TOPIC_ERROR,
            'max_length':LONG_TOPIC_ERROR})
    start_date_time = forms.DateTimeField(required=True, 
            error_messages={
            'required': EMPTY_START_DATE_TIME_ERROR,
            })
    end_date_time = forms.DateTimeField(required=True,
                error_messages={
            'required': EMPTY_END_DATE_TIME_ERROR,
            })
    #venue = forms.CharField(required=True)
    venue = forms.ModelChoiceField(queryset=Room.objects.all(), label='Venue', widget=forms.Select(attrs={'class':'form-control'}))
    no_of_available_seat = forms.IntegerField(required=True)

    class Meta:
        model = Seminar
        fields = ['topic', 'start_date_time', 'end_date_time', 'venue', 'no_of_available_seat']

    def clean(self):
        new_end_date_time = self.cleaned_data.get('end_date_time')
        new_start_date_time = self.cleaned_data.get('start_date_time')
        no_of_available_seat = self.cleaned_data.get('no_of_available_seat')
        new_venue = self.cleaned_data.get('venue')
        
        if not(no_of_available_seat is None):
            if (no_of_available_seat <= 0):
                raise ValidationError(
                    INVALID_NO_OF_AVAILABLE_SEAT_ERROR)

        # This ensures the seminar is still have vacancy.
        if not(new_end_date_time is None or new_start_date_time is None):
            if ( new_end_date_time <= new_start_date_time ):
                raise ValidationError(
                    INVALID_SEMINAR_START_END_DATETIME_ERROR)       

            conflicts = Seminar.objects.filter(
                start_date_time__lt=new_end_date_time,
                end_date_time__gt=new_start_date_time, 
                venue=new_venue
            )
            if self.instance.pk is not None:
                conflicts = conflicts.exclude(pk=self.instance.pk)

            if any(conflicts):
                raise forms.ValidationError(INVALID_SEMINAR_DATE_RANGE_ERROR)

            conflicts = Seminar.objects.filter(
                start_date_time__lt=new_start_date_time,
                end_date_time__gt=new_end_date_time, 
                venue=new_venue
            )
            if self.instance.pk is not None:
                conflicts = conflicts.exclude(pk=self.instance.pk)

            if any(conflicts):
                raise forms.ValidationError(INVALID_SEMINAR_DATE_RANGE_ERROR)
        return self.cleaned_data

class BookingForm(forms.Form):
    seminar_id = forms.IntegerField()

    def clean(self):
        seminar_id = self.cleaned_data.get('seminar_id')
        seminar = Seminar.objects.get(pk=seminar_id)
        
        # This ensures the seminar is still have vacancy.
        if ( seminar.no_of_available_seat <= 0 ):
            raise ValidationError(
                SEMINAR_FULL_ERROR)       
        else:
            return self.cleaned_data 