from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

# Create your views here.
class BookList(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        books = Book.objects.all()
        return books
