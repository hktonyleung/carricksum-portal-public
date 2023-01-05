from datetime import date
from .base._managers import BaseModelManager

class AnnouncementManager(BaseModelManager):
    def get_active_announcement(self):
        return super(AnnouncementManager, self).get_queryset().filter(expired_datetime__date__gt=date.today())