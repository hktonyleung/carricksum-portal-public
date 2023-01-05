from django.contrib import admin
from portal.admin import BaseAdmin
from .models import Post

# Register your models here.
class PostAdmin(BaseAdmin):
    list_display = ('topic', 'intro', 'deleted')
    search_fields = ('topic', 'intro')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Post, PostAdmin)
