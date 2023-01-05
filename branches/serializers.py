"""Markers serializers."""

from rest_framework_gis import serializers

from branches.models import Branch

class BranchesSerializer(serializers.GeoFeatureModelSerializer):
    """Branch GeoJSON serializer."""

    class Meta:
        """Branch serializer meta class."""

        fields = ("id", "name", "desc")
        #fields = ("name", "desc")
        geo_field = "geo"
        model = Branch

