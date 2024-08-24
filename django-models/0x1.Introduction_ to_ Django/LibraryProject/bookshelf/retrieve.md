# Retrieving a Book from the Database

## Overview

This document explains how to retrieve a book from the database using Django's ORM (Object-Relational Mapping).

## Retrieving a Book by Title

To retrieve a book with the title "1984," use the following Django ORM command:

```python
from bookshelf.models import Book

# Retrieve the book with the title "1984"
retrieved_book = Book.objects.get(title="1984")
print(retrieved_book)  # Expected output: 1984 by George Orwell (1949)
