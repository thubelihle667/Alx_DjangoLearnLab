>>>from bookshelf.models import Book
>>>mybook = Book.objects.all().delete()
>>> mybook.title 
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'title'
>>> mybook.author
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'author'
>>> mybook.publication_year
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'publication_year'      
>>> mybook = Book.objects.all()
>>> mybook
<QuerySet []>
>>> print(mybook.query)
SELECT "bookshelf_book"."id", "bookshelf_book"."title", "bookshelf_book"."author", "bookshelf_book"."publication_year" FROM "bookshelf_book"    
>>>
