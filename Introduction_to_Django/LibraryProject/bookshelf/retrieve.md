from bookshelf.models import Book

mybook_data = Book.objects.all()
mybook_data  # Will give the following output <QuerySet [<Book: Book object (1)>]> 
print(mybook_data.query)  # Will give the following output:SELECT "bookshelf_book"."id", "bookshelf_book"."title", "bookshelf_book"."author", "bookshelf_book"."publication_year" FROM "bookshelf_book" which are attributes of mybook instance.
