from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)  # Title with a max length of 200 characters
    author = models.CharField(max_length=100)  # Author with a max length of 100 characters
    publication_year = models.IntegerField()     # Publication year as an integer

    def __str__(self):
        return self.title  # Returns the book title when the object is printed
