"""Markers API views."""
from rest_framework import viewsets
from rest_framework_gis import filters

from .models import Branch
from .serializers import BranchesSerializer
from django.contrib.auth.mixins import LoginRequiredMixin

class BranchesViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    """Polygon view set."""

    bbox_filter_field = "geo"
    filter_backends = (filters.InBBoxFilter,)
    queryset = Branch.objects.all()
    serializer_class = BranchesSerializer