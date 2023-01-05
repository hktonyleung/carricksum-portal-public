from django.test import TestCase

from blogs.models import Post
from portal.models import User

class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(username='testuser', password='123456')
        Post.objects.create(
            topic='Test Case Topic', 
            intro='What is Test Case?', 
            content='Test Case is ....... and ........',
            created_by=user,
        )

    def test_topic(self):
        post = Post.objects.get(id=1)
        topic = post.topic
        self.assertEqual(topic, 'Test Case Topic')

'''
    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        url = post.get_absolete_url()
        self.assertEqual(url, '/blogs/1/')

    def test_get_edit_url(self):
        post = Post.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        url = post.get_edit_url()
        self.assertEqual(url, '/blogs/1/update')
'''
