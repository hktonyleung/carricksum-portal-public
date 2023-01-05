from django.db import models
from portal.base._models import BaseModel
from django.conf import settings
from django.urls import reverse
from report.managers import ReportManager, ReportTypeManager
from cloudinary_storage.storage import RawMediaCloudinaryStorage

REPORT_STATUS = (
    ("RE", "READY"),
    ("GE", "GENERATING"),
    ("CO", "COMPLETED"),
)

class ReportType(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=4)
    template_path = models.CharField(max_length=100)

    def __str__(self):
        return self.name    

    class Meta:
        ordering = ['name'] 

    objects = ReportTypeManager()
    all_objects = ReportTypeManager(alive_only=False)

class Report(BaseModel):
    name = models.CharField(max_length=100)
    generate_start_date = models.DateTimeField(blank=True, null=True)
    generate_end_date = models.DateTimeField(blank=True, null=True)
    pdf = models.FileField(null=True, blank=True) #to be delete
    raw_file = models.ImageField(upload_to='raw/', blank=True, storage=RawMediaCloudinaryStorage())
    type = models.ForeignKey(ReportType, on_delete=models.CASCADE, related_name="report_report_type", blank=True, null=True)

    status = models.CharField(
        max_length=2,
        choices=REPORT_STATUS,
        default="RE",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name'] 

    objects = ReportManager()
    all_objects = ReportManager(alive_only=False)

    
