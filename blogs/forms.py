from django import forms
from django.forms import ModelForm
from .models import Post
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE


EMPTY_TOPIC_ERROR = "Topic should be input"
EMPTY_INTRO_ERROR = "Introduction should be input"
EMPTY_CONTENT_ERROR = "Content should be input"
LONG_TOPIC_ERROR = "Topic is too long"
LONG_INTRO_ERROR = "Introcution is too long"
LONG_CONTENT_ERROR = "Content is too long"


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class PostForm(ModelForm):

    topic = forms.CharField(required=True, label='Topic', 
        error_messages={
            'required': EMPTY_TOPIC_ERROR,
            'max_length':LONG_TOPIC_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Topic'}))
    intro = forms.CharField(required=True, label='Introduction',
        error_messages={'required': EMPTY_INTRO_ERROR, 
        'max_length':LONG_INTRO_ERROR},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Introduction'}))
    content = forms.CharField(
        error_messages={
            'required': EMPTY_CONTENT_ERROR,
            'max_length':LONG_CONTENT_ERROR},
        widget=TinyMCEWidget(
            attrs={'cols': 50, 'rows': 10}))

    class Meta:
        model = Post
        fields = ['topic', 'intro', 'content', 'tags']


        
            
        