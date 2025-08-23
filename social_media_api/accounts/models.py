from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    # Followers: other users who follow THIS user
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following_users',
        blank=True,
    )

    # Users this user follows
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers_users",
        blank=True,
        help_text="Users that this user is following"
    )

    def __str__(self):
        return self.username

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()
