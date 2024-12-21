from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

User = get_user_model()

# ViewSet for Post
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'content']  # Enable searching by title or content

    # Ensure the user can only create posts with their own user as the author
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Ensure the user can only see their own posts
        return Post.objects.filter(author=self.request.user)

# ViewSet for Comment
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    # Ensure the user can only create comments with their own user as the author
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Ensure the user can only see their own comments on posts they created
        return Comment.objects.filter(author=self.request.user)
