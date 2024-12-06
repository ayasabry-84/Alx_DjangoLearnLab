from django.urls import path 
from .views import register, profile, user_logout
from django.contrib.auth.views import LoginView, LogoutView
from .views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

app_name = 'blog'

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='post_list'),  # List of posts
    path('post/<int:pk>/', views.BlogPostDetailView.as_view(), name='post_detail'),  # Post detail
    path('post/new/', views.BlogPostCreateView.as_view(), name='post_create'),  # Create post
    path('post/<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='post_update'),  # Update post
    path('post/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='post_delete'),  # Delete post

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', user_logout, name='user_logout'),

]
