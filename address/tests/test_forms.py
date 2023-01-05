from django.test import TestCase
from address.forms import AddressForm
from address.forms import (EMPTY_BUILDING_NAME_ERROR, LONG_BUILDING_NAME_ERROR, EMPTY_STREET_NAME_ERROR, 
                            LONG_STREET_NAME_ERROR, EMPTY_BUILDING_NO_FROM_ERROR, LONG_BUILDING_NO_FROM_ERROR, 
                            EMPTY_BUILDING_NO_TO_ERROR, LONG_BUILDING_NO_TO_ERROR, EMPTY_DISTRICT_ERROR, 
                            LONG_DISTRICT_ERROR, EMPTY_FULL_ADDRESS_ERROR, LONG_FULL_ADDRESS_ERROR, 
                            EMPTY_RELATED_DOCUMENT_ERROR, LONG_RELATED_DOCUMENT_ERROR)
from portal.models import User
from address.models import Address
from django.forms.forms import NON_FIELD_ERRORS

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

class AddressFormTest(TestCase):

    def test_form_valid_for_buildingName(self):
        form = AddressForm(
            data={'buildingName': '', 'streetName':'', 'buildingNoFrom':'', 
                    'buildingNoTo':'', 'district':'','fullAddress':'','relatedDocument':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['buildingName'], [EMPTY_BUILDING_NAME_ERROR])
        self.assertEqual(form.errors['streetName'], [EMPTY_STREET_NAME_ERROR])
        self.assertEqual(form.errors['buildingNoFrom'], [EMPTY_BUILDING_NO_FROM_ERROR])
        self.assertEqual(form.errors['buildingNoTo'], [EMPTY_BUILDING_NO_TO_ERROR])
        self.assertEqual(form.errors['district'], [EMPTY_DISTRICT_ERROR])
        self.assertEqual(form.errors['fullAddress'], [EMPTY_FULL_ADDRESS_ERROR])
        self.assertEqual(form.errors['relatedDocument'], [EMPTY_RELATED_DOCUMENT_ERROR])

    def test_form_valid_for_long_buildingName(self):
        form = AddressForm(
            data={'buildingName': '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890', 
                    'streetName':'', 
                    'buildingNoFrom':'', 
                    'buildingNoTo':'', 
                    'district':'',
                    'fullAddress':'',
                    'relatedDocument':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['buildingName'], [LONG_BUILDING_NAME_ERROR])
        
    def test_form_valid_for_long_streetName(self):
        form = AddressForm(
            data={'buildingName': '', 
                    'streetName':'12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890', 
                    'buildingNoFrom':'', 
                    'buildingNoTo':'', 
                    'district':'',
                    'fullAddress':'',
                    'relatedDocument':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['streetName'], [LONG_STREET_NAME_ERROR])

    def test_form_valid_for_long_buildingNoFrom(self):
        form = AddressForm(
            data={'buildingName': '', 
                    'streetName':'', 
                    'buildingNoFrom':'12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890', 
                    'buildingNoTo':'', 
                    'district':'',
                    'fullAddress':'',
                    'relatedDocument':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['buildingNoFrom'], [LONG_BUILDING_NO_FROM_ERROR])

    def test_form_valid_for_long_buildingNoFrom(self):
        form = AddressForm(
            data={'buildingName': '', 
                    'streetName':'', 
                    'buildingNoFrom':'12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890', 
                    'buildingNoTo':'', 
                    'district':'',
                    'fullAddress':'',
                    'relatedDocument':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['buildingNoFrom'], [LONG_BUILDING_NO_FROM_ERROR])

    def test_form_valid_for_long_buildingNoTo(self):
        form = AddressForm(
            data={'buildingName': '', 
                    'streetName':'', 
                    'buildingNoFrom':'', 
                    'buildingNoTo':'12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890', 
                    'district':'',
                    'fullAddress':'',
                    'relatedDocument':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['buildingNoTo'], [LONG_BUILDING_NO_TO_ERROR])

    def test_form_valid_for_long_district(self):
        form = AddressForm(
            data={'buildingName': '', 
                    'streetName':'', 
                    'buildingNoFrom':'', 
                    'buildingNoTo':'', 
                    'district':'12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890',
                    'fullAddress':'',
                    'relatedDocument':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['district'], [LONG_DISTRICT_ERROR])

    def test_form_valid_for_long_fullAddress(self):

        form = AddressForm(
            data={'buildingName': '1234567890', 
                    'streetName':'1234567890', 
                    'buildingNoFrom':'12345', 
                    'buildingNoTo':'12345', 
                    'district':'1234567890',
                    'fullAddress':'12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890',
                    'relatedDocument':'1234567890'}, 
            files={'uploadFile': image})
        self.assertTrue(form.is_valid())
        #self.assertEqual(form.errors['fullAddress'], [LONG_FULL_ADDRESS_ERROR])

    def test_form_valid_for_long_relatedDocument(self):

        form = AddressForm(
            data={'buildingName': '1234567890', 
                    'streetName':'1234567890', 
                    'buildingNoFrom':'12345', 
                    'buildingNoTo':'12345', 
                    'district':'1234567890',
                    'fullAddress':'1234567890',
                    'relatedDocument':'12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'}, 
            files={'uploadFile': image})
        self.assertTrue(form.is_valid())
        #self.assertEqual(form.errors['relatedDocument'], [LONG_RELATED_DOCUMENT_ERROR])