from django.urls import path
from .views import register, profile, user_logout
from django.contrib.auth.views import LoginView, LogoutView
from .views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

app_name = 'blog'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', user_logout, name='user_logout'),

    path('', BlogPostListView.as_view(), name='post_list'), # Home page or post list
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='post_detail'), # Post details
    path('post/new/', BlogPostCreateView.as_view(), name='post_create'), # Create new post
    path('post/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='post_edit'), # Edit post
    path('post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='post_delete'), # Delete post

]
