from rest_framework import generics
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

from rest_framework.viewsets import ModelViewSet


from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

class MyView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def get(self, request):
        return Response({"message": "Hello, authenticated user!"})

class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]  # Only admin users can access this view

    def get(self, request):
        return Response({"message": "Hello, admin user!"})






class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookList(generics.ListAPIView):
    queryset = Book.objects.all() 
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]