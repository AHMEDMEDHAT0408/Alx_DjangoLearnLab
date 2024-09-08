from rest_framework import serializers
from .models import Author, Book

# Serializer for the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    # Custom validation to ensure the publication year is not in the future
    def validate_publication_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# Serializer for the Author model, including related books
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
# Author model represents an author of multiple books.
# The related_name='books' allows reverse querying from Author to Book.

# Book model represents a book that has a title, publication year, and is related to an Author.
# The foreign key establishes a one-to-many relationship with the Author model.

# In serializers.py:
# AuthorSerializer includes a nested BookSerializer to serialize related books.
# BookSerializer includes a custom validation for ensuring publication year is valid.
