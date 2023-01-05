from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

class BaseQuerySet(QuerySet):
    def delete(self):
        return super(BaseQuerySet, self).update(deleted_at=timezone.now(), deleted=True)

    def hard_delete(self):
        return super(BaseQuerySet, self).delete()

class BaseModelManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(BaseModelManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return BaseQuerySet(self.model).filter(deleted_at=None)
        return BaseQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()