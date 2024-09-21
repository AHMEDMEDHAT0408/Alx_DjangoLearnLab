from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters
from rest_framework import status
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from accounts.models import CustomUser
from notifications.models import Notification  # Assuming you have a Notification model for notifications

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


# View to like a post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user

    # Check if the user has already liked the post
    if Like.objects.filter(post=post, user=user).exists():
        return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a like
    like = Like.objects.create(post=post, user=user)

    # Create a notification for the post author
    Notification.objects.create(
        recipient=post.author,
        actor=user,
        verb='liked your post',
        target=post
    )

    return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)


# View to unlike a post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user

    # Check if the user has liked the post
    like = Like.objects.filter(post=post, user=user).first()
    if not like:
        return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

    # Delete the like
    like.delete()

    return Response({'detail': 'Post unliked successfully.'}, status=status.HTTP_200_OK)
