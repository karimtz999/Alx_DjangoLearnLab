from django.urls import path
from .views import ListView, DetailView, CreateView, UpdateView, DeleteView

urlpatterns = [
    path('books/', ListView.as_view(), name='book-list'),  # List all books
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),  # Retrieve a single book
    path('books/create/', CreateView.as_view(), name='book-create'),  # Create a new book
    path('books/<int:pk>/update/', UpdateView.as_view(), name='book-update'),  # Update an existing book
    path('books/<int:pk>/delete/', DeleteView.as_view(), name='book-delete'),  # Delete a book
]
