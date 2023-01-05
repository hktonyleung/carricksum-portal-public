from rest_framework import serializers

from address.models import Address

'''
class AddressSerializer(serializers.ModelSerializer):

    uploadFile_url = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ['buildingName', 'streetName', 
                    'buildingNoFrom', 'buildingNoTo', 
                    'district', 'fullAddress', 'relatedDocument', 
                    'uploadFile_url',]

    def get_uploadFile_url(self, address):
        request = self.context.get('request')
        uploadFile_url = address.uploadFile
        return request.build_absolute_uri(uploadFile_url)        
'''
class AddressSerializer(serializers.Serializer):

    buildingName = serializers.CharField(max_length=200)
    streetName = serializers.CharField(max_length=200)
    buildingNoFrom = serializers.CharField(max_length=200)
    buildingNoTo = serializers.CharField(max_length=200)
    district = serializers.CharField(max_length=200)
    fullAddress = serializers.CharField(max_length=200)
    relatedDocument = serializers.CharField(max_length=200)
    uploadFile = serializers.CharField(max_length=200)