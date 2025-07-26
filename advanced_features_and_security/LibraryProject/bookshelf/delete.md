>>>from bookshelf.models import Book
>>> mybook = Book.objects.get(title="Nineteen Eighty-Four")
>>> mybook.delete()   # Book instance is deleted
