from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns for posts, registration, profile, etc.
    
    # URL for listing all posts
    path('', views.PostListView.as_view(), name='post-list'),

    # URL for a single post's details
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

    # URL for creating a new post
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),

    # URL for updating an existing post
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),

    # URL for deleting a post
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # URL for creating a new comment on a post
    path('post/<int:pk>/comments/new/', views.add_comment, name='comment-create'),

    # URL for updating a comment
    path('comment/<int:pk>/update/', views.update_comment, name='comment-update'),

    # URL for deleting a comment
    path('comment/<int:pk>/delete/', views.delete_comment, name='comment-delete'),
]
