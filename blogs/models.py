from tinymce.models import HTMLField
from django.db import models
from portal.base._models import BaseModel
from django.conf import settings
from django.urls import reverse
#from taggit.managers import TaggableManager
from taggit_selectize.managers import TaggableManager

class Post(BaseModel):
    topic = models.CharField(max_length=100)
    intro = models.CharField(max_length=500)
    content =  HTMLField()
    #created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_created_by")
    tags = TaggableManager(verbose_name="Tags",help_text="A comma-separated list of tags.",blank=True)

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ('-updated_datetime',)    

'''
    def get_absolete_url(self):
        return reverse('blogs:post-detail', args=[str(self.id)])

    def get_edit_url(self):
        return reverse('blogs:post-update', args=[str(self.id)])
'''


