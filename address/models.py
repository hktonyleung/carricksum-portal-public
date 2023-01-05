from django.db import models
from portal.base._models import BaseModel
from address.managers import AddressManager
from cloudinary_storage.storage import RawMediaCloudinaryStorage


# Create your models here.
class Address(BaseModel):

    buildingName = models.CharField(max_length=100)
    streetName = models.CharField(max_length=100)
    buildingNoFrom = models.CharField(max_length=5, blank=True, null=True)
    buildingNoTo = models.CharField(max_length=5, blank=True, null=True)
    district = models.CharField(max_length=100)
    fullAddress = models.CharField(max_length=4000, blank=True, null=True)
    relatedDocument = models.CharField(max_length=200, blank=True, null=True) 
    uploadFile = models.FileField(upload_to='address/', blank=True, null=True, storage=RawMediaCloudinaryStorage())

    def __str__(self):
        return self.buildingName

    objects = AddressManager()
    all_objects = AddressManager(alive_only=False) 
