from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book
from .serializers import BookSerializer

class BookAPITests(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create some sample data
        self.book1 = Book.objects.create(title='Book One', author='Author One', publication_year=2021, price=10.00)
        self.book2 = Book.objects.create(title='Book Two', author='Author Two', publication_year=2022, price=15.00)
        
    def test_list_books(self):
        response = self.client.get('/api/books/')
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        data = {
            'title': 'Book Three',
            'author': 'Author Three',
            'publication_year': 2023,
            'price': 20.00
        }
        response = self.client.post('/api/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'Book Three')

    def test_update_book(self):
        data = {'title': 'Updated Book One'}
        response = self.client.patch(f'/api/books/{self.book1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(id=self.book1.id).title, 'Updated Book One')

    def test_delete_book(self):
        response = self.client.delete(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books(self):
        response = self.client.get('/api/books/', {'author': 'Author Two'})
        serializer = BookSerializer(Book.objects.filter(author='Author Two'), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search_books(self):
        response = self.client.get('/api/books/', {'search': 'Book Two'})
        serializer = BookSerializer(Book.objects.filter(title='Book Two'), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_ordering_books(self):
        response = self.client.get('/api/books/', {'ordering': 'title'})
        serializer = BookSerializer(Book.objects.all().order_by('title'), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
