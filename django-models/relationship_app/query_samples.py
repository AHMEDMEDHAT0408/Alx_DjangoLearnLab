from .models import Author, Book
from .models import Library, Librarian
def get_books_by_author(author_name):
    # Get the author object by name
    author = Author.objects.get(name=author_name)
    
    # Use objects.filter() to get all books by the specific author
    books = Book.objects.filter(author=author)

    # Print the titles of the books
    for book in books:
        print(book.title)


# List all books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()

    for book in books:
        print(book.title)


# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    # Get the library object by name
    library = Library.objects.get(name=library_name)
    
    # Use objects.get() to retrieve the librarian associated with the library
    librarian = Librarian.objects.get(library=library)

    # Print the name of the librarian
    print(librarian.name)
