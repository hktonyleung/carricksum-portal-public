
from django.urls import path
from . import views
from blogs.views import PostListView, PostDetailView, PostUpdateView, PostCreateView, PostDeleteView, TaggedPostView

app_name = 'blogs'

urlpatterns = [
    path("", PostListView.as_view(), name="post-index"),
    path('<str:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<str:pk>/update', PostUpdateView.as_view(), name='post-update'), 
    path('create', PostCreateView.as_view(), name='post-create'),
    path('<str:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('tagged/<slug>', TaggedPostView.as_view(), name='tagged'),
]