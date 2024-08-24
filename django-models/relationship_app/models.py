from django.db import models

# Author model representing a book author
class Author(models.Model):
    name = models.CharField(max_length=100)  # Name of the author

    def __str__(self):
        return self.name


# Book model representing a book, linked to an author
class Book(models.Model):
    title = models.CharField(max_length=200)  # Title of the book
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')  # ForeignKey linking to Author

    def __str__(self):
        return self.title


# Library model representing a collection of books
class Library(models.Model):
    name = models.CharField(max_length=100)  # Name of the library
    books = models.ManyToManyField(Book, related_name='libraries')  # ManyToMany relationship with Book

    def __str__(self):
        return self.name


# Librarian model representing the manager of a library
class Librarian(models.Model):
    name = models.CharField(max_length=100)  # Name of the librarian
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')  # OneToOne relationship with Library

    def __str__(self):
        return self.name
