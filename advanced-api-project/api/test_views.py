from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Book

class BookAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book_data = {'title': 'Test Book', 'author': 'Author', 'description': 'A test book', 'price': 10.99}
        self.url = reverse('book-list')

    # Test book creation
    def test_create_book(self):
        response = self.client.post(self.url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.book_data['title'])

    # Test getting list of books
    def test_get_books(self):
        Book.objects.create(title="Test Book", author="Author", description="A test book", price=10.99)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # Test retrieving a single book by ID
    def test_get_book_detail(self):
        book = Book.objects.create(title="Test Book", author="Author", description="A test book", price=10.99)
        url = reverse('book-detail', kwargs={'pk': book.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], book.title)

    # Test updating a book
    def test_update_book(self):
        book = Book.objects.create(title="Test Book", author="Author", description="A test book", price=10.99)
        url = reverse('book-detail', kwargs={'pk': book.id})
        updated_data = {'title': 'Updated Book', 'author': 'Updated Author', 'price': 15.99}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book')

    # Test deleting a book
    def test_delete_book(self):
        book = Book.objects.create(title="Test Book", author="Author", description="A test book", price=10.99)
        url = reverse('book-detail', kwargs={'pk': book.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book.id).exists())

    # Test filtering by author
    def test_filter_books_by_author(self):
        Book.objects.create(title="Book 1", author="Author A", description="Desc", price=10.99)
        Book.objects.create(title="Book 2", author="Author B", description="Desc", price=12.99)
        url = f'{self.url}?author=Author A'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Test searching by title
    def test_search_books(self):
        Book.objects.create(title="Searchable Book", author="Author", description="Desc", price=10.99)
        url = f'{self.url}?search=Searchable'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # Test ordering by title
    def test_order_books_by_title(self):
        Book.objects.create(title="A Book", author="Author A", description="Desc", price=10.99)
        Book.objects.create(title="Z Book", author="Author B", description="Desc", price=12.99)
        url = f'{self.url}?ordering=title'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "A Book")
