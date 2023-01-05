from django.test import TestCase
from address.models import Address
from portal.models import User

class AddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='testuser', password='123456')
        Address.objects.create(
            buildingName='Building Name 1', 
            streetName='Street Name 1', 
            buildingNoFrom='101', 
            buildingNoTo='201', 
            district='District 1', 
            fullAddress='Full Address 1', 
            relatedDocument='Related Document 1',             
            created_by=user,
        )

    def test_buildingName(self):
        address = Address.objects.get(id=1)
        buildingName = address.buildingName
        self.assertEqual(buildingName, 'Building Name 1')

    def test_streetName(self):
        address = Address.objects.get(id=1)
        streetName = address.streetName
        self.assertEqual(streetName, 'Street Name 1')

    def test_buildingNoFrom(self):
        address = Address.objects.get(id=1)
        buildingNoFrom = address.buildingNoFrom
        self.assertEqual(buildingNoFrom, '101')

    def test_buildingNoTo(self):
        address = Address.objects.get(id=1)
        buildingNoTo = address.buildingNoTo
        self.assertEqual(buildingNoTo, '201')

    def test_district(self):
        address = Address.objects.get(id=1)
        district = address.district
        self.assertEqual(district, 'District 1')

    def test_fullAddress(self):
        address = Address.objects.get(id=1)
        fullAddress = address.fullAddress
        self.assertEqual(fullAddress, 'Full Address 1')

    def test_relatedDocument(self):
        address = Address.objects.get(id=1)
        relatedDocument = address.relatedDocument
        self.assertEqual(relatedDocument, 'Related Document 1')
