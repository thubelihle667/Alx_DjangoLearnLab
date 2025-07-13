from bookshelf.models import Book

mybook = Book.objects.create(title="1984",author="George Orwell",publication_year=1949)

mybook.title   # Will give an output of "1984"
mybook.author  # Wll give an output of "George Orwell"
mybook.publication_year  # Will give an output of 1949

