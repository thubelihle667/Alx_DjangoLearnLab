python manage.py shell

from relationship_app.models import Author,Book,Library,Librarian

books = Library.objects.get(name=library_name)
books.all()

book = Author.objects.get(name=author_name)
objects.filter(author=author)

book = Librarian.objects.get(library='')
