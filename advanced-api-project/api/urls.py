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
    path('create_book/', CustomBookCreateView.as_view(), name='create_book'),
    path('delete_book/', CustomBookDeleteView.as_view(), name='delete_book'),
    path('update_book/', CustomBookUpdateView.as_view(), name='update_book'),
]