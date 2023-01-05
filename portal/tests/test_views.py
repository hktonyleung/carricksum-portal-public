from django.test import TestCase
from django.urls import reverse

from portal.models import Announcement, User

class AnnouncementIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_announcements = 3
        user = User.objects.create_user(username='testuser', password='123456')
        user.save()

        for announcement_id in range(number_of_announcements):        
            Announcement.objects.create(
                subject=f'Test Announcement {announcement_id}', 
                text=f'This is test announcement {announcement_id}',
                created_by=user
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/login?next=/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('index'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'portal/index.html')

        # check if announcemnts in response context
        self.assertTrue('announcements' in response.context)

        # check if announcemnts count in response context
        self.assertTrue('announcement_count' in response.context)    

        # check if announcements count value is correct
        self.assertEqual(int(response.context['announcement_count']), 3)     

