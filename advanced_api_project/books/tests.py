from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book
from django.contrib.auth.models import User

class BookAPITests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            published_date='2024-01-01',
            isbn='1234567890123'
        )
        
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', args=[self.book.id])

    def test_create_book(self):
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'published_date': '2024-01-02',
            'isbn': '9876543210987'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.latest('id').title, 'New Book')

    def test_read_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_update_book(self):
        data = {'title': 'Updated Book', 'isbn': '1234567890987'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
        self.assertEqual(self.book.isbn, '1234567890987')

    def test_delete_book(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_filter_books(self):
        response = self.client.get(self.list_url, {'author': 'Test Author'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        response = self.client.get(self.list_url, {'search': 'Test Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        response = self.client.get(self.list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = response.data
        self.assertTrue(books[0]['title'] <= books[1]['title'])
