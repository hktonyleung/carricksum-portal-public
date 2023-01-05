from django.contrib import admin
from portal.base._admin import BaseAdmin
from report.models import Report, ReportType

# Register your models here.
class ReportTypeAdmin(BaseAdmin):
    list_display = ('name', 'template_path')
    search_fields = ('name', 'template_path')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ReportAdmin(BaseAdmin):
    list_display = ('name', 'status', 'created_by')
    search_fields = ('name', 'status')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(ReportType, ReportTypeAdmin)
admin.site.register(Report, ReportAdmin)