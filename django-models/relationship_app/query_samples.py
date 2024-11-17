from relationship_app.models import Author, Book

# Query all books by a specific author
def get_books_by_author(author_name):
    try:
        # Get the author instance directly
        author = Author.objects.get(name=author_name)  # Ensure we retrieve the correct author
    except Author.DoesNotExist:
        return None  # Return None if the author does not exist

    # Use the author's related name to retrieve books
    books = Book.objects.filter(author=author)
    return books
