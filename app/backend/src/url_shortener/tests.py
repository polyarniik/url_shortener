from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase
from django.urls import reverse

from url_shortener.models import URL

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test123", password="test123")

    def tearDown(self) -> None:
        self.user.delete()

    def test_wrong_username(self):
        user = authenticate(username="wrong", password="test123")
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username="test123", password="wrong")
        self.assertFalse(user is not None and user.is_authenticated)


class SignInViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="12test12")

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        response = self.client.post(
            reverse("main:login"), {"username": "test", "password": "12test12"}
        )
        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )

    def test_wrong_username(self):
        response = self.client.post(
            reverse("main:login"), {"username": "wrong", "password": "12test12"}
        )
        self.assertEqual(response.status_code, 403)

    def test_wrong_password(self):
        response = self.client.post(
            reverse("main:login"), {"username": "test", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 403)


class URLTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test123", password="test123")

    def test_creating(self) -> None:
        url = URL.objects.create(url="www.google.com", user=self.user)
        self.assertFalse(url.id is None)

    def test_redirect(self) -> None:
        url = URL.objects.create(url="www.google.com", user=self.user)
        response = self.client.get(
            reverse("main:short_url", kwargs={"short": url.short_url})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], url.url)
