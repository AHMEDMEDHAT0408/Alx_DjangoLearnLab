from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm
from .models import Post, Comment
from django.db.models import Q
from taggit.models import Tag

# Search Functionality
def search(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    else:
        posts = Post.objects.none()

    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})

# List posts filtered by tag
class PostByTagListView(ListView):  # Renamed this class to match the URL pattern requirement
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get('tag_slug'))
        return Post.objects.filter(tags=tag).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag_slug')
        return context

# Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# User Profile View
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})

# Blog Post Views for CRUD Operations
# List View for all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Specify your own template
    context_object_name = 'posts'
    ordering = ['-date_posted']  # Display newest posts first

# Detail View for a single post with comments
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # Specify your own template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()  # Fetch comments related to the post
        context['form'] = CommentForm()  # Provide a comment form for authenticated users
        return context

# Create View for a new post (only for authenticated users)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']  # Define the fields to show in the form
    template_name = 'blog/post_form.html'

    # Overriding form_valid to associate the logged-in user as the author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update View for editing an existing post (only for the post author)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']  # Define the fields to show in the form
    template_name = 'blog/post_form.html'

    # Overriding form_valid to ensure the correct author is maintained
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Check if the current user is the author of the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete View for deleting a post (only for the post author)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')  # Redirect to the post list after deletion

    # Check if the current user is the author of the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Comment Views
# Create a comment for a specific post
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})

# Update a comment (only by the comment's author)
@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('post-detail', pk=comment.post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/update_comment.html', {'form': form})

# Delete a comment (only by the comment's author)
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    if request.user == comment.author:
        comment.delete()
    return redirect('post-detail', pk=post_id)
