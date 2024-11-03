# Delete Book

**Command:**
```python
from bookshelf.models import Book

# Retrieve the book you want to delete
book_to_delete = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book_to_delete.delete()

# Confirm deletion by trying to retrieve all books again
books_after_deletion = Book.objects.all()
print(books_after_deletion)  # Should show an empty queryset if the deletion was successful

