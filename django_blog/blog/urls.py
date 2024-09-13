# In blog/urls.py
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    register, profile, add_comment, update_comment, delete_comment,
    search, PostByTagListView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_id>/comment/', add_comment, name='add-comment'),
    path('comment/<int:pk>/update/', update_comment, name='update-comment'),
    path('comment/<int:pk>/delete/', delete_comment, name='delete-comment'),

    # Correct path using PostByTagListView
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts-by-tag'),
    path('search/', search, name='search'),
]
