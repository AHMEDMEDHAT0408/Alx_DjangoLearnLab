# Deleting a Book from the Database

## Overview

This document explains how to delete a book from the database using Django's ORM (Object-Relational Mapping).

## Steps to Delete a Book

1. **Import the Model**

   Import the `Book` model from your application’s models module.

   ```python
   from bookshelf.models import Book
# Retrieve the book instance
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book instance
book.delete()
try:
    retrieved_book = Book.objects.get(title="Nineteen Eighty-Four")
except Book.DoesNotExist:
    print("Book has been successfully deleted.")  # Expected output
