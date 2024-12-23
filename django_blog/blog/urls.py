from django.urls import path 
from . import views
from .views import register, profile, user_logout
from django.contrib.auth.views import LoginView, LogoutView
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from django.contrib.auth import views as auth_views  # Add this import


app_name = 'blog'

urlpatterns = [

    # Home page or other views
    #path('', views.home, name='home'),

    path('', views.PostListView.as_view(), name='post_list'),  # List of posts
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),  # Post detail
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),  # Create post
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),  # Update post
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),  # Delete post

    path('register/', views.register, name='register'),  # Custom register view
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Login URL
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout view (built-in)

    path('profile/', views.profile, name='profile'),  # Custom profile view

    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='edit_comment'),  # Edit comment URL
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),  # Delete comment URL

    path('search/', views.search_posts, name='search_posts'),
    path('tags/<str:tag_name>/', views.posts_by_tag, name='tag_posts'),

    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts_by_tag'),
]
