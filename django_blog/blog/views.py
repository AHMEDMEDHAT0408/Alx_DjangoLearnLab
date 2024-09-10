from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserUpdateForm
from .models import Post

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

# Detail View for a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # Specify your own template

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
