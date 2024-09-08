from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter

class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title']

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]
