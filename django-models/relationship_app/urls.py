from django.urls import path
from . import views
from .views import LibraryDetailView

urlpatterns = [
    path('books/', views.list_books, name='list_books'),  # URL for the function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),# URL for the class-based view
]
