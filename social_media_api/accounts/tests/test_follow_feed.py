# tests/test_follow_feed.py
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from posts.models import Post

User = get_user_model()

class FollowFeedTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username="alice", password="pass123")
        self.u2 = User.objects.create_user(username="bob", password="pass123")
        self.u3 = User.objects.create_user(username="charlie", password="pass123")

        # Posts by followed/non-followed users
        self.p2 = Post.objects.create(author=self.u2, content="bob post 1")
        self.p3 = Post.objects.create(author=self.u3, content="charlie post 1")

        self.follow_url = lambda uid: reverse("follow-user", kwargs={"user_id": uid})
        self.unfollow_url = lambda uid: reverse("unfollow-user", kwargs={"user_id": uid})
        self.feed_url = reverse("feed")

        # Authenticate as u1
        self.client.force_authenticate(user=self.u1)

    def test_follow_user(self):
        res = self.client.post(self.follow_url(self.u2.id))
        self.assertIn(res.status_code, [200, 201])
        self.assertTrue(self.u1.following.filter(pk=self.u2.id).exists())

    def test_unfollow_user(self):
        self.u1.following.add(self.u2)
        res = self.client.delete(self.unfollow_url(self.u2.id))
        self.assertEqual(res.status_code, 204)
        self.assertFalse(self.u1.following.filter(pk=self.u2.id).exists())

    def test_cannot_follow_self(self):
        res = self.client.post(self.follow_url(self.u1.id))
        self.assertEqual(res.status_code, 400)

    def test_feed_shows_only_followed_users(self):
        # Initially u1 follows no one → empty feed
        res = self.client.get(self.feed_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data.get("results", res.data)), 0)

        # Follow u2 (bob) → feed should include bob's post, not charlie's
        self.client.post(self.follow_url(self.u2.id))
        res = self.client.get(self.feed_url)
        self.assertEqual(res.status_code, 200)
        payload = res.data.get("results", res.data)
        post_ids = [item["id"] for item in payload]
        self.assertIn(self.p2.id, post_ids)
        self.assertNotIn(self.p3.id, post_ids)
