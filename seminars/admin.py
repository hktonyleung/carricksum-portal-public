from django.contrib import admin
from portal.base._admin import BaseAdmin
from seminars.models import Room, Seminar, Booking

# Register your models here.
class RoomAdmin(BaseAdmin):
    list_display = ('no', 'desc')
    search_fields = ('no', 'desc')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class SeminarAdmin(BaseAdmin):
    list_display = ('topic', 'start_date_time', 'end_date_time', 'venue', 'no_of_available_seat', 'deleted')
    search_fields = ('topic', 'venue')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class BookingAdmin(admin.ModelAdmin):
    list_display = ('seminar', 'attendee','unique_string')
    search_fields = ('seminar', 'attendee')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Room, RoomAdmin)
admin.site.register(Seminar, SeminarAdmin)
admin.site.register(Booking, BookingAdmin)