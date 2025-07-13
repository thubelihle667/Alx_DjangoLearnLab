from bookshel.models import Book

mybook = Book.objects.get(title="1984")

mybook.title # Will give an output of '1984'
mybook.author # Will give an output of 'George Orwell'
mybook.publication_year  #will give an output of 1949
