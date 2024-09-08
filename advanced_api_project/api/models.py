from django.db import models

# Author model representing an author of books
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Book model representing a book and linking to an author
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
# Author model represents an author of multiple books.
# The related_name='books' allows reverse querying from Author to Book.

# Book model represents a book that has a title, publication year, and is related to an Author.
# The foreign key establishes a one-to-many relationship with the Author model.

# In serializers.py:
# AuthorSerializer includes a nested BookSerializer to serialize related books.
# BookSerializer includes a custom validation for ensuring publication year is valid.
