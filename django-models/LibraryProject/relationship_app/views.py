from django.shortcuts import render
from .models import Book

# Create your views here.
def book_list(request):
      """Retrieves all books and renders a template displaying the list."""
      books = Book.objects.all()  
      context = {'list_book': books}  
      return render(request, 'list_books.html', context)

from django.views.generic import DetailView
from .models import Book

class BookDetailView(DetailView):
  model = Book
  template_name = 'books/book_detail.html'