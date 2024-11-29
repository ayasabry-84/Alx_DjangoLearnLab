from django.db import models


class Author(models.Model):
    # The Author model stores the details of an author.
    # It has a single field: 'name', which stores the author's name.
    # Each author can have multiple books associated with them, establishing a one-to-many relationship with the Book model.

    name = models.CharField(max_length=200)  # The name of the author (max 200 characters)

    def __str__(self):
        return self.name  # Returns the author's name when an Author object is printed or displayed


class Book(models.Model):
    # The Book model stores details about each book.
    # It includes a title, a publication year, and a relationship to the Author model (via ForeignKey).
    # A book must always be associated with an author, as the ForeignKey enforces a many-to-one relationship between Book and Author.

    title = models.CharField(max_length=200)  # The title of the book (max 200 characters)
    publication_year = models.DateField()  # The publication year of the book as a DateField
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Each book is associated with one Author

    def __str__(self):
        return self.title  # Returns the book's title when a Book object is printed or displayed
