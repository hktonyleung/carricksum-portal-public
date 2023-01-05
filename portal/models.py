from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from .base._models import BaseModel
from .managers import AnnouncementManager
from django.utils.timezone import now
from portal.utils import one_weeks_later

class User(AbstractUser):
    pass

class Announcement(BaseModel):
    subject = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcement_author")
    expired_datetime = models.DateTimeField(default=one_weeks_later)
    #expired_datetime = models.DateTimeField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.subject} ({self.created.strftime("%Y-%m-%d")})'

    objects = AnnouncementManager()
    all_objects = AnnouncementManager(alive_only=False) 