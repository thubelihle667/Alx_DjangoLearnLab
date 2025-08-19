from django.urls import path
from .views import RegisterView, LoginView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='accounts-register'),
    path('login/', LoginView.as_view(), name='accounts-login'),
    path('profile/', ProfileView.as_view(), name='accounts-profile'),
]

