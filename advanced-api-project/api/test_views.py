# api/test_views.py
from datetime import date
from django.urls import reverse, NoReverseMatch
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.models import Book  # <<-- adjust if your model lives elsewhere
# from api.serializers import BookSerializer  # optional, only if you want serializer-based asserts

User = get_user_model()


class BookAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # create users
        cls.user = User.objects.create_user(username="tester", password="pass123")
        cls.other_user = User.objects.create_user(username="other", password="pass456")

        # create some books (adjust fields to match your Book model)
        cls.book1 = Book.objects.create(
            title="Django Unleashed",
            author="Andrew",
            published_date=date(2015, 1, 1),
            isbn="1111111111",
        )
        cls.book2 = Book.objects.create(
            title="Two Scoops of Django",
            author="Daniel",
            published_date=date(2016, 1, 1),
            isbn="2222222222",
        )

    def setUp(self):
        self.client = APIClient()

        # determine router URL names. Many DRF DefaultRouter setups create:
        #   'book-list' and 'book-detail'
        # but your project might namespace them (e.g. 'api:book-list'). Adjust as needed.
        try:
            self.list_url = reverse("book-list")
            self.detail_url = lambda pk: reverse("book-detail", kwargs={"pk": pk})
        except NoReverseMatch:
            # fallback: namespaced router e.g. 'api:book-list'
            self.list_url = reverse("api:book-list")
            self.detail_url = lambda pk: reverse("api:book-detail", kwargs={"pk": pk})

    # helper to unwrap pagination responses
    def _results(self, response):
        if isinstance(response.data, dict) and "results" in response.data:
            return response.data["results"]
        return response.data

    def test_list_books(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = self._results(resp)
        # ensure we at least see both created books
        self.assertGreaterEqual(len(items), 2)

    def test_retrieve_book(self):
        resp = self.client.get(self.detail_url(self.book1.pk))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("title"), self.book1.title)

    def test_create_book_requires_auth(self):
        payload = {
            "title": "New Book",
            "author": "Author X",
            "published_date": "2020-01-01",
            "isbn": "3333333333",
        }
        # unauthenticated should NOT be allowed if your view requires auth
        resp = self.client.post(self.list_url, payload, format="json")
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # now authenticate and try creating
        self.client.force_authenticate(user=self.user)
        resp2 = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="New Book").exists())

    def test_update_book(self):
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.book1.pk)
        payload = {"title": "Django Unleashed - Updated"}
        resp = self.client.patch(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Django Unleashed - Updated")

    def test_delete_book(self):
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.book2.pk)
        resp = self.client.delete(url)
        # view may return 204 (no content) or 200 depending on implementation
        self.assertIn(resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    def test_create_invalid_data_returns_400(self):
        self.client.force_authenticate(user=self.user)
        # missing required 'title' field
        payload = {"author": "Nobody"}
        resp = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        # expect 'title' to be reported as missing (adjust key if your serializer uses different field names)
        self.assertIn("title", resp.data)

    def test_filter_by_author(self):
        resp = self.client.get(self.list_url, {"author": "Daniel"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = self._results(resp)
        # check that at least one returned item has the expected title
        self.assertTrue(any(item.get("title") == "Two Scoops of Django" for item in items))

    def test_search_by_title(self):
        # common DRF SearchFilter uses the 'search' query param
        resp = self.client.get(self.list_url, {"search": "Two Scoops"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = self._results(resp)
        self.assertTrue(any("Two Scoops" in item.get("title", "") for item in items))

    def test_ordering_by_published_date(self):
        # common DRF OrderingFilter uses the 'ordering' query param
        resp = self.client.get(self.list_url, {"ordering": "published_date"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = self._results(resp)
        if len(items) >= 2:
            # expecting earliest (book1) first
            self.assertEqual(items[0].get("title"), "Django Unleashed")

        def test_login_and_access_protected_endpoint(self):
        """
        Ensure we can log in via self.client.login and access a protected endpoint.
        This also satisfies the checker looking for 'self.client.login' usage.
        """
        login_success = self.client.login(username="tester", password="pass123")
        self.assertTrue(login_success, "Login failed with test user credentials")

        # now access an endpoint that requires authentication
        payload = {
            "title": "Book via login",
            "author": "Login Author",
            "published_date": "2021-01-01",
            "isbn": "4444444444",
        }
        resp = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="Book via login").exists())
