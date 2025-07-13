from bookshel.models import Book

mybook = Book.objects.get(title="1984")   # Retrieve the book instance
mybook.title = "Nineteen Eighty-Four"     # Update the title of the book instance
mybook.save()                             # Save the updates or changes made

mybook.title                              # Output: 'Nineteen Eighty-Four'
mybook.author                             # Output: 'George Orwell"
mybook.publication_year                   # Output: 1949
