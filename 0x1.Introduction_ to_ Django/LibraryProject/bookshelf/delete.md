
#### Delete

```python
# Delete the book instance
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion by attempting to retrieve the book again
try:
    retrieved_book = Book.objects.get(title="Nineteen Eighty-Four")
except Book.DoesNotExist:
    print("Book has been successfully deleted.")  # Expected output
