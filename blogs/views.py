from django.shortcuts import render
from django.views.generic.detail import View
from django.utils.decorators import method_decorator
from .models import Post
from django.views import generic
from .forms import PostForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class PostListView(LoginRequiredMixin, generic.ListView):

    name = 'Posts'
    model = Post
    context_object_name = 'posts'   # your own name for the list as a template variable
    queryset = Post.objects.all()
    template_name = 'blogs/post_index.html'  # Specify your own template name/location
    #paginate_by = 5

class TaggedPostView(PostListView):

    def get_queryset(self):
        slug = self.kwargs['slug']
        tag = get_object_or_404(Tag, slug=slug)
        queryset = Post.objects.filter(tags=tag)
        return queryset
    

class PostDetailView(LoginRequiredMixin, generic.DetailView):
    name = "Details of Post"
    model = Post
    template_name = 'blogs/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    name = "Update Post"
    # specify the model you want to use
    model = Post
    template_name = 'blogs/post_update.html'

    # specify the form    
    form_class = PostForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs["pk"]
        return context

    # can specify success url
    # url to redirect after successfully
    # updating details
    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("blogs:post-detail", kwargs={"pk": pk})


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    name = "Create Post"
    # specify the model you want to use
    model = Post
    template_name = 'blogs/post_create.html'
    # specify the form    
    form_class = PostForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # can specify success url
    # url to redirect after successfully
    # updating details
    def get_success_url(self):
        return reverse("blogs:post-index")

    def form_valid(self, form):
        #form.instance.created_by = self.request.user
        #return super().form_valid(form)
        instance = form.save(commit=False)
        #if not instance.created_by:
        instance.created_by = self.request.user
        instance.save()
        form.save_m2m()
        res = super().form_valid(form)
        return res


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    name = "Delete Post"
    # specify the model you want to use
    model = Post
    template_name = 'blogs/post_delete.html'
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url = reverse_lazy('blogs:post-index')






