# Update Book

**Command:**
```python
from bookshelf.models import Book

# Retrieve the book you want to update
book_to_update = Book.objects.get(title="1984")

# Update the title of the book instance
book_to_update.title = "Nineteen Eighty-Four"  # This line updates the title
book_to_update.save()  # Save the changes to the database
