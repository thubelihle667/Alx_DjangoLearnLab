from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Author, Book, Library, Librarian
from django.contrib.auth.views import LoginView

def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

