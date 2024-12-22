from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post, Like
from accounts.models import CustomUser 
from notifications.models import Notification
from django.shortcuts import get_object_or_404


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
    

class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        feed_data = [
            {
                'id': post.id,
                'author': post.author.username,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
            }
            for post in posts
        ]
        return Response(feed_data)

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = get_object_or_404(Post, id=post_id)
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if created:
                # إنشاء إشعار
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb="liked your post",
                    target=post
                )
                return Response({"message": "Post liked successfully."})
            else:
                return Response({"message": "You already liked this post."}, status=400)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=404)

class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = get_object_or_404(Post, id=post_id)
            like = Like.objects.filter(user=request.user, post=post)
            if like.exists():
                like.delete()
                return Response({"message": "Post unliked successfully."})
            else:
                return Response({"message": "You have not liked this post."}, status=400)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=404)