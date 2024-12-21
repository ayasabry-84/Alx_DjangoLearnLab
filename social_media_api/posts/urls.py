from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

# Create Router to connect the ViewSets
router = DefaultRouter()

# Register the ViewSets with the router
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

# Add URLs to the application
urlpatterns = [
    path('', include(router.urls)),  # Connect the viewsets with URLs
]
