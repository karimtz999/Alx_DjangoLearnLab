# api/filters.py
import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'title': ['icontains'],  # Allows filtering by title (case-insensitive)
            'author__name': ['icontains'],  # Filter by author's name (case-insensitive)
            'publication_year': ['exact'],  # Filter by exact publication year
        }
