from ast import Pass
from django.contrib import admin
from django.contrib.gis import admin

class BaseAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = self.model.all_objects
        # The below is copied from the base implementation in BaseModelAdmin to prevent other changes in behavior
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        obj.hard_delete()

class BaseGeoAdmin(admin.OSMGeoAdmin, BaseAdmin):
    Pass
