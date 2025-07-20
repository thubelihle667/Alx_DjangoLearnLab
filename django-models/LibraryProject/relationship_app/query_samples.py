python manage.py shell

from relationship_app.models import Author,Book,Library,Librarian

books_query_by_author = Book.objects.get(title='')
all_books_list = Library.objects.all()
librarian = Librarian.objects.get(name='')
