from django.urls import path
from .views import list_books
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('books/', views.list_books, name='book_list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='registration/login.html')),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html')),
    path('register/', views.register, name='register'),
]
