from django.db import models
from ._managers import BaseModelManager
from django.utils import timezone
from django.conf import settings

class BaseModel(models.Model): 
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_created_by")

    class Meta:
        abstract = True

    objects = BaseModelManager()
    all_objects = BaseModelManager(alive_only=False)

    def delete(self):
        self.deleted_at = timezone.now()
        self.deleted = True
        self.save()

    def hard_delete(self):
        super(BaseModel, self).delete()