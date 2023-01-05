from django.test import TestCase
from portal.models import Announcement, User
from portal.utils import one_weeks_later
from django.utils import dateformat

class AnnouncementModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='testuser', password='123456')
        Announcement.objects.create(
            subject='Test Announcement', 
            text='This is test announcement', 
            created_by=user,
        )

    def test_subject(self):
        announcement = Announcement.objects.get(id=1)
        subject = announcement.subject
        self.assertEqual(subject, 'Test Announcement')
    
    def test_text(self):
        announcement = Announcement.objects.get(id=1)
        text = announcement.text
        self.assertEqual(text, 'This is test announcement')        

    def test_created_by(self):
        announcement = Announcement.objects.get(id=1)
        user = User.objects.last()
        created_by = announcement.created_by
        self.assertEqual(created_by, user) 

    def test_expired_datetime(self):
        announcement = Announcement.objects.get(id=1)
        expired_datetime = announcement.expired_datetime
        self.assertAlmostEqual(
            expired_datetime.replace(hour=0, minute=0, second=0, microsecond=0), 
            one_weeks_later().replace(hour=0, minute=0, second=0, microsecond=0))
