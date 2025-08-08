from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer



# Create your views here.
class CustomBookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_class = [IsAuthenticatedOrReadOnly]

class CustomBookDetailView(generics.DetailAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_class = [IsAuthenticated]

class CustomBookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_class = [IsAuthenticated]

class CustomBookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_class = [IsAuthenticated]

class CustomBookDeleteView(generics.DeleteAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_class = [IsAuthenticated]