from django.urls import path
from .views import BookListView, api_root, BookDetailView

urlpatterns = [
    path('', api_root, name='api-root'),  # Root URL for /api/
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]
