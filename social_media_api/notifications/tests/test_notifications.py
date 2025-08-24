from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from notifications.models import Notification

User = get_user_model()

class NotificationTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='alice', password='pass')
        self.u2 = User.objects.create_user(username='bob', password='pass')
        self.client.force_authenticate(user=self.u2)
        self.index_url = reverse('notifications')

    def test_list_notifications(self):
        Notification.objects.create(recipient=self.u2, actor=self.u1, verb='started following you')
        res = self.client.get(self.index_url)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data.get('results', res.data)), 1)

    def test_mark_read(self):
        n = Notification.objects.create(recipient=self.u2, actor=self.u1, verb='started following you')
        mark_url = reverse('notification-read', kwargs={'pk': n.id})
        res = self.client.post(mark_url)
        self.assertEqual(res.status_code, 200)
        n.refresh_from_db()
        self.assertTrue(n.is_read)
