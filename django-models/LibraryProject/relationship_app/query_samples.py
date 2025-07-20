python manage.py shell

from relationship_app.models import Author,Book,Library,Librarian

books = Library.objects.get(name=library_name)
books.all()
all_books_list = Library.objects.all()
librarian = Librarian.objects.get(name='')
