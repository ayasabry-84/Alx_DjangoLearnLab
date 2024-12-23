# relationship_app/urls.py
from django.urls import path
from .views import list_books, LibraryDetailView  # Import the function-based view and class-based view
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('books/', list_books, name='list_books'),  # Function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.register, name='register'),
     path('admin/', views.admin_view, name='admin_view'),
]
