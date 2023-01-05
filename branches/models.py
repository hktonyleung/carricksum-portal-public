from django.db import models
from portal.base._models import BaseModel
from branches.managers import BranchManager
from django.contrib.gis.db import models

# Create your models here.

class Branch(BaseModel):
    name = models.CharField(max_length=20)
    desc = models.CharField(max_length=40)
    active = models.BooleanField(default=False)
    geo = models.PolygonField(null=True)


    def __str__(self):
        return self.name

    objects = BranchManager()
    all_objects = BranchManager(alive_only=False) 
