# api/test_views.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book
from django.contrib.auth.models import User

class BookFilterTests(APITestCase):
    
    def setUp(self):
        # Creating sample books for testing filtering, searching, and ordering
        self.book1 = Book.objects.create(title='Book A', author='Author A', publication_year=2020)
        self.book2 = Book.objects.create(title='Book B', author='Author B', publication_year=2021)
        self.book3 = Book.objects.create(title='Book C', author='Author A', publication_year=2022)

    def test_filter_by_author(self):
        # Test filtering books by author name
        url = reverse('book-list') + '?author__name=Author A'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two books by 'Author A'

    def test_search_by_title(self):
        # Test searching books by title
        url = reverse('book-list') + '?search=Book A'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one book with 'Book A' title

    def test_order_by_publication_year(self):
        # Test ordering books by publication year
        url = reverse('book-list') + '?ordering=publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert the first book has the earliest publication year
        self.assertEqual(response.data[0]['publication_year'], 2020)
