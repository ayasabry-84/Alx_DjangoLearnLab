# Update Book

**Command:**
```python
from bookshelf.models import Book

# Retrieve the book you want to update
book = Book.objects.get(title="1984")

# Update the title of the book instance
book.title = "Nineteen Eighty-Four"  
book.save()  # Save the changes to the database
