from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post

User = get_user_model()

class PostCommentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass1234")
        self.other = User.objects.create_user(username="bob", password="pass1234")
        self.client.login(username="alice", password="pass1234")

    def test_create_post(self):
        url = reverse("post-list")
        data = {"title": "Test Title", "content": "Body text here"}
        res = self.client.post(url, data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().author, self.user)

    def test_list_posts(self):
        Post.objects.create(author=self.user, title="A", content="x")
        Post.objects.create(author=self.user, title="B", content="y")
        url = reverse("post-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data.get("results", res.data)), 2)

    def test_owner_can_edit_own_post_but_not_others(self):
        post = Post.objects.create(author=self.user, title="Mine", content="x")
        url = reverse("post-detail", args=[post.id])
        res = self.client.patch(url, {"title": "Updated"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # switch to another user
        self.client.logout()
        self.client.login(username="bob", password="pass1234")
        res = self.client.patch(url, {"title": "Bob edits"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

