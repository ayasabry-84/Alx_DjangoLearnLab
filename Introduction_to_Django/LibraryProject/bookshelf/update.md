# Update Book

**Command:**
```python
from bookshelf.models import Book

# Retrieve the book you want to update
book_to_update = Book.objects.get(title="1984")

# Update the title
book_to_update.title = "Nineteen Eighty-Four"  # Update the title of the book
book_to_update.save()  # Save the changes
