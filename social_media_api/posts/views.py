from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters
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


# Feed View to get posts from followed users
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):
    user = request.user
    followed_users = user.following.all()  # Get the users that the current user is following
    posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
