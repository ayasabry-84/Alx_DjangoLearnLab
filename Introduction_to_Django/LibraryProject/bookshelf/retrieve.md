# Retrieve Book

**Command:**
```python
from bookshelf.models import Book

# Retrieve all Book instances
books = Book.objects.all()

# Display all attributes of the first book in the queryset
for book in books:
    print(f"Title: {book.title}, Author: {book.author}, Publication Year: {book.publication_year}")

