from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Announcement
from seminars.models import Seminar

@receiver(post_save, sender=Seminar)
def create_seminar_announcement(sender, instance, created, **kwargs):
    if created:
        Announcement.objects.create(
            subject="New Seminar: " + instance.topic,
            text="From: " + instance.start_date_time.strftime("%m/%d/%Y %H:%M") + " To: " + instance.end_date_time.strftime("%m/%d/%Y %H:%M"),
            created_by=instance.created_by)
