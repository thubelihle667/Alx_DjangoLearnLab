from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from posts.models import Post, Like
from notifications.models import Notification

User = get_user_model()

class LikeTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='alice', password='pass')
        self.u2 = User.objects.create_user(username='bob', password='pass')
        self.post = Post.objects.create(author=self.u2, content='hello')
        self.like_url = reverse('post-like', kwargs={'pk': self.post.id})
        self.unlike_url = reverse('post-unlike', kwargs={'pk': self.post.id})
        self.client.force_authenticate(user=self.u1)

    def test_like_creates_notification(self):
        res = self.client.post(self.like_url)
        self.assertIn(res.status_code, [200, 201])
        self.assertTrue(Like.objects.filter(user=self.u1, post=self.post).exists())
        self.assertTrue(Notification.objects.filter(recipient=self.u2, actor=self.u1, verb__icontains='liked').exists())

    def test_like_idempotent(self):
        self.client.post(self.like_url)
        res = self.client.post(self.like_url)
        self.assertIn(res.status_code, [200, 201])
        self.assertEqual(Like.objects.filter(user=self.u1, post=self.post).count(), 1)

    def test_unlike(self):
        self.client.post(self.like_url)
        res = self.client.delete(self.unlike_url)
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Like.objects.filter(user=self.u1, post=self.post).exists())
