from django import forms
from .models import Author, Book, Library, Librarian

class AuthorForm(forms.ModelForm):
    class Meta:
        name = Author
        fields = ['name']

class BookForm(forms.ModelForm):
    class Meta:
        name = Book
        fields = ['title', 'author']

class LibraryForm(forms.ModelForm):
    class Meta:
        name = Library
        fields = ['name', 'books']

class LibrarianForm(forms.ModelForm):
    class Meta:
        name = Librarian
        fields = ['name', 'library']