## Updating a Book

To update the title of a book instance, use the following command:

```python
# Update the title of the book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book)  # Expected output: Nineteen Eighty-Four by George Orwell (1949)
