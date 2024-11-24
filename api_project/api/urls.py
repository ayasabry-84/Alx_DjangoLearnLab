from django.urls import path
from .views import BookListCreateAPIView
from .views import BookList


urlpatterns = [
    path("api/books", BookListCreateAPIView.as_view(), name="book_list_create"),
    path('books/', BookList.as_view(), name='book-list'),
]