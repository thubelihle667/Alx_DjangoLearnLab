from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

# Create your views here.
class BookList(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        books = Book.objects.all()
        return books

class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer