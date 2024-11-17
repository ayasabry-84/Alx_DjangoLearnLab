from django.shortcuts import render
from .models import Book
from django.views.generic.detail import DetailView
from .models import Library

def list_books(request):
    books = Book.objects.all()  # Fetch all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})  # Render the books in the template


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
