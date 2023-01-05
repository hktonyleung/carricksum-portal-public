"""Markers API URL Configuration."""

from rest_framework import routers

from .api_views import BranchesViewSet

router = routers.DefaultRouter()
router.register(r"branches", BranchesViewSet)

urlpatterns = router.urls