from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

class CustomUser(AbstractUser):
    date_of_birth = models.DateField()
    profile_photo = models.ImageField(upload_to='images/', blank=True)
    email = models.EmailField(unique=True, max_length=200)
    username = models.CharField(unique=False, max_length=150)

    USERNAME_FIELD = "email"
    REQUIRED_FIELD = []

    objects = UserManager()

class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("Users must have an email")

            user = self.models(email=self.normalize_email())
            user.set_password(password)
            user.save(using=self._db)

            return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)

        user.is_staff = True
        user.is_superuser = True
        user.save(useing=self._db)

        return user    