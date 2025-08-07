from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

# Create your views here.
class CustomBookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CustomBookDetailView(generics.DetailAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CustomBookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CustomBookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CustomBookDeleteView(generics.DeleteAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer