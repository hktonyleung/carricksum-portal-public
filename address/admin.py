from django.contrib import admin
from portal.base._admin import BaseAdmin
from address.models import Address

# Register your models here.
class AddressAdmin(BaseAdmin):
    list_display = ('buildingName', 'streetName','buildingNoFrom','buildingNoTo','district','fullAddress')
    search_fields = ('buildingName', 'fullAddress')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Address, AddressAdmin)
