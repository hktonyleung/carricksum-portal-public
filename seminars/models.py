from django.db import models
from portal.base._models import BaseModel
from seminars.managers import BookingManager, RoomManager, SeminarManager, BookingManager
from django.db.models import Func, Q
from django.conf import settings
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import (
    DateTimeRangeField,
    RangeBoundary,
    RangeOperators,
)


SEMINAR_STATUS = (
    ("OP", "OPEN"),
    ("CA", "CANCEL"),
)

class TsTzRange(Func):
    function = 'TSTZRANGE'
    output_field = DateTimeRangeField()

# Create your models here.
class Room(BaseModel):
    no = models.CharField(max_length=20, unique=True)
    desc = models.CharField(max_length=100)
    
    def __str__(self):
        return self.no

    class Meta:
        ordering = ['no'] 

    objects = RoomManager()
    all_objects = RoomManager(alive_only=False)

class Seminar(BaseModel):
    topic = models.CharField(max_length=100)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    venue = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="seminar_venue")
    no_of_available_seat = models.PositiveIntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seminar_created_by")
    status = models.CharField(
        max_length=2,
        choices=SEMINAR_STATUS,
        default="OP",
    )

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ['-start_date_time']
        constraints = [
            ExclusionConstraint(
                name='exclude_overlapping_reservations',
                expressions=(
                    (TsTzRange('start_date_time', 'end_date_time', RangeBoundary()), RangeOperators.OVERLAPS),
                    ('venue', RangeOperators.EQUAL),
                ),
                condition=Q(status="OP"),
            ),
        ]

    objects = SeminarManager()
    all_objects = SeminarManager(alive_only=False) 

class Booking(BaseModel):
    seminar = models.ForeignKey(Seminar, on_delete=models.CASCADE, related_name="booking_seminar")
    attendee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="booking_attendee")
    unique_string = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.seminar.topic} by {self.attendee}'

    class Meta:
        unique_together = ('seminar', 'attendee',)

    objects = BookingManager()
    all_objects = BookingManager(alive_only=False) 