from django.urls import path
from .views import [
    CustomBookCreateView,
    CustomBookDeleteView,
    CustomBookDetailView,
    CustomBookListView,
    CustomBookUpdateView,
]

urlpatterns = [
    path('books/', CustomBookListView.as_view(),name='list_books'),
    path('books/<int:pk>/', CustomBookDetailView.as_view(), name='book_details'),
    path('books/create', CustomBookCreateView.as_view(), name='create_book'),
    path('books/delete', CustomBookDeleteView.as_view(), name='delete_book'),
    path('books/update', CustomBookUpdateView.as_view(), name='update_book'),
]