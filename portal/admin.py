from django.contrib import admin
from .base._admin import BaseAdmin
from django.contrib.auth.admin import UserAdmin
from .models import User, Announcement

# Register your models here.
class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class AnnouncementAdmin(BaseAdmin):
    list_display = ('subject', 'text', 'created', 'created_by', 'deleted')
    search_fields = ('subject', 'text')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(User, UserAdmin)