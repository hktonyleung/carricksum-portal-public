#from django.contrib import admin
from django.contrib.gis import admin
from portal.base._admin import BaseGeoAdmin
from branches.models import Branch

# Register your models here.
#class BranchAdmin(admin.OSMGeoAdmin):
class BranchAdmin(BaseGeoAdmin):
    list_display = ('name', 'desc','deleted')
    search_fields = ('name', 'desc')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Branch, BranchAdmin)