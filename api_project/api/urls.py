from django.urls import path , include
from .views import BookListCreateAPIView
from .views import BookList , BookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path("api/books", BookListCreateAPIView.as_view(), name="book_list_create"),
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
]

