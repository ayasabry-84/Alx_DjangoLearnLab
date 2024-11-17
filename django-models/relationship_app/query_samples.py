from relationship_app.models import Author, Book

# Query all books by a specific author
def get_books_by_author(author_name):
    try:
        # Combine the author retrieval and book filtering
        return Book.objects.filter(author=Author.objects.get(name=author_name))
    except Author.DoesNotExist:
        return None
