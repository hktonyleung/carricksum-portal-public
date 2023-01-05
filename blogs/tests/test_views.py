from django.test import TestCase
from django.urls import reverse

from blogs.models import Post
from portal.models import User

from http import HTTPStatus

class PostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_posts = 3

        user = User.objects.create_user(username='testuser', password='123456')

        for post_id in range(number_of_posts):
            post = Post.objects.create(
                topic=f'Test Case Topic {post_id}', 
                intro=f'What is Test Case? {post_id}', 
                content=f'Test Case is ....... and ........ {post_id}',
                created_by=user,
            )
            print(post.id)


    def test_post_list_view_by_location(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.get('/blogs/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test PostListView
    def test_post_list_view_by_name(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('blogs:post-index'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Check we used correct template
        self.assertTemplateUsed(response, 'blogs/post_index.html')

        self.assertEqual(len(response.context['posts']), 3)  

    # Test PostDetailView 
    def test_post_detail_view_if_not_logged_in(self):
        response = self.client.get('/blogs/2/')
        self.assertRedirects(response, '/login?next=/blogs/2/')

    # Test PostDetailView
    def test_post_detail_view_by_location(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.get('/blogs/2/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test PostDetailView
    def test_post_detail_view_by_name(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('blogs:post-detail', args=[2]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test PostCreateView 
    def test_post_create_view_if_not_logged_in(self):
        response = self.client.get('/blogs/create')
        self.assertRedirects(response, '/login?next=/blogs/create') 

    # Test PostCreateView
    def test_post_create_view_by_location(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.get('/blogs/create')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test PostCreateView
    def test_post_create_view_by_name(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('blogs:post-create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test PostCreateView
    def test_post_create_view_post_create(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.post(reverse('blogs:post-create'),
            data={'topic':'Testing', 'intro':'Introduction', 'content':'Content'})
        self.assertRedirects(response, reverse('blogs:post-index'))
        cnt = Post.objects.count()
        self.assertEqual(cnt, 4)

   # Test PostUpdateView 
    def test_post_update_view_if_not_logged_in(self):
        response = self.client.get('/blogs/2/update')
        self.assertRedirects(response, '/login?next=/blogs/2/update') 

    # Test PostUpdateView
    def test_post_update_view_by_location(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.get('/blogs/2/update')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test PostUpdateView
    def test_post_update_view_by_name(self):
        login = self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('blogs:post-update', args=[2]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Test PostUpdateView
    def test_post_update_view_post_update(self):
        login = self.client.login(username='testuser', password='123456')
        user = User.objects.get(username='testuser')
        post = Post.objects.create(
            topic='Testing-update',
            intro='Introduction-update',
            content='Content-update',
            created_by=user,
        )
        response = self.client.post(
            reverse('blogs:post-update', kwargs = {
                'pk': post.id
                }), {
                    'topic': 'Testing-updated',
                    'intro': 'Introduction-updated',
                    'content':'Content-updated'
                })
        self.assertRedirects(response, reverse("blogs:post-detail", kwargs={"pk": post.id}))
        is_exists = Post.objects.filter(topic='Testing-updated').exists()
        self.assertEqual(is_exists, True)