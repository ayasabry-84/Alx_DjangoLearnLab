# Retrieve Book

**Command:**
```python
from bookshelf.models import Book

# Retrieve the book instance using objects.get() by title
book = Book.objects.get(title="1984")

# Display all attributes of the retrieved book
print(f"Title: {book.title}, Author: {book.author}, Publication Year: {book.publication_year}")
