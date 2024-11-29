from rest_framework import serializers
from .models import Book
from .models import Author
from datetime import datetime

# The BookSerializer is responsible for converting Book model instances into JSON data and vice versa.
# It includes fields for the title, publication year, and the associated author.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book  # Specifies that this serializer is for the Book model
        fields = '__all__'  # Include all fields from the Book model (title, publication_year, author)

    def validate_publication_year(self, value):
        """
        Custom validation to ensure publication_year is not in the future.
        The validation checks that the publication year is less than or equal to the current year.
        """
        current_year = datetime.now().year  # Get the current year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# The AuthorSerializer is responsible for converting Author model instances into JSON data and vice versa.
# It includes fields for the author's name and a list of books associated with the author.
# The 'Book' field is nested using the BookSerializer to represent the books related to an author.
class AuthorSerializer(serializers.ModelSerializer):
    # A nested serializer for the Book model to include all books of an author
    Book = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author  # Specifies that this serializer is for the Author model
        fields = '__all__'  # Include all fields from the Author model (name and related books)

