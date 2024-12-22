from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from .views import FeedView
from .views import LikePostView, UnlikePostView


# Create Router to connect the ViewSets
router = DefaultRouter()

# Register the ViewSets with the router
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

# Add URLs to the application
urlpatterns = [
    path('', include(router.urls)),  # Connect the viewsets with URLs
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]
