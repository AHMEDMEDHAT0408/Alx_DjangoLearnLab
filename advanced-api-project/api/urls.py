from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    # List all books and create a new book
    path('books/', BookListView.as_view(), name='book-list'),

    # Retrieve, update, and delete a single book
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # Create a new book
    path('books/create/', BookCreateView.as_view(), name='book-create'),

    # Update an existing book
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),  # Ensure this exists

    # Delete a book
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),  # Ensure this exists
]
