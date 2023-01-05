from django.test import TestCase
from django.urls import reverse

from address.models import Address
from portal.models import User

from http import HTTPStatus

from PIL import Image
from io import BytesIO # Python 2: from StringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

im = Image.new(mode='RGB', size=(200, 200)) # create a new image using PIL
im_io = BytesIO() # a BytesIO object for saving image
im.save(im_io, 'JPEG') # save the image to im_io
im_io.seek(0) # seek to the beginning

image = InMemoryUploadedFile(
    im_io, None, 'random-name.jpg', 'image/jpeg', len(im_io.getvalue()), None
)

class AddressViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_addresses = 3

        user = User.objects.create_superuser(username='testuser', password='123456')
        for address_id in range(number_of_addresses):
            address = Address.objects.create(
                buildingName=f'Building Name {address_id}', 
                streetName=f'Street Name {address_id}', 
                buildingNoFrom='100', 
                buildingNoTo='200', 
                district=f'District {address_id}', 
                fullAddress=f'Full Address {address_id}', 
                relatedDocument=f'Related Document {address_id}',          
                created_by=user,
            )
        
    def test_address_list_view_by_location(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.get('/address/addresses')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test PostListView
    def test_address_list_view_by_name(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('address:address-manage'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Check we used correct template
        self.assertTemplateUsed(response, 'address/address_index.html')

        self.assertEqual(len(response.context['addresses']), 3)  

    def test_address_create(self):
        login = self.client.login(username='testuser', password='123456')
        #address = Address.objects.get(id=1)
        response = self.client.post('/address/addresses/create', {
            'buildingName':'Building Name 4', 
            'streetName':'Street Name 4', 
            'buildingNoFrom':'104', 
            'buildingNoTo':'204', 
            'district':'District 4', 
            'fullAddress':'Full Address 4', 
            'relatedDocument':'Related Document 4', 
            'uploadFile':image})
        no_of_address = Address.objects.count()
        self.assertEqual(no_of_address, 4)

    def test_address_update(self):
        login = self.client.login(username='testuser', password='123456')

        address = Address.objects.last()
        print(address.id)
        response = self.client.post('/address/addresses/'+ str(address.id) +'/update', {
            'buildingName':'Building Name 3-Updated', 
            'streetName':'Street Name 3', 
            'buildingNoFrom':'103', 
            'buildingNoTo':'203', 
            'district':'District 3', 
            'fullAddress':'Full Address 3', 
            'relatedDocument':'Related Document 3'})
        address = Address.objects.get(id=address.id)
        buildingName = address.buildingName
        print(buildingName)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(buildingName, 'Building Name 3-Updated')
        
    def test_address_delete(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.post('/address/addresses/2/delete')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        no_of_address = Address.objects.count()
        self.assertEqual(no_of_address, 2)

