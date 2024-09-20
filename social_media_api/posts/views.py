from rest_framework import viewsets, permissions, filters, generics
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from accounts.models import CustomUser  # Import CustomUser to check following relationships

# Post ViewSet for managing CRUD operations on posts
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    # Automatically assign the post author as the currently logged-in user
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Comment ViewSet for managing CRUD operations on comments
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Automatically assign the comment author and the related post
    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)


# Class-based view for the user feed to get posts from followed users
class UserFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    # Retrieve posts from users the current user is following
    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()  # Get the list of users the current user follows
        return Post.objects.filter(author__in=following_users).order_by('-created_at')  # Fetch posts by followed users, ordered by creation date
