from django.urls import path
from .views import list_books, LibraryDetailView  # Import both views

urlpatterns = [
    path('books/', list_books, name='list_books'),  # URL pattern for function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # URL pattern for class-based view
]
