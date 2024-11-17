from relationship_app.models import Author, Book

# Query all books by a specific author
def get_books_by_author(author_name):
    try:
        # Retrieve the author
        author = Author.objects.get(name=author_name)
        # Filter books by this author
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return None
