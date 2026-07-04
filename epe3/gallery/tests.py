from django.test import TestCase
from django.urls import reverse


class AuthEmailFallbackTests(TestCase):
    def test_registration_shows_activation_link_when_email_backend_is_unavailable(self):
        response = self.client.post(
            reverse("register"),
            {"username": "tester", "email": "tester@example.com", "password": "secret123"},
            follow=True,
        )
        self.assertContains(response, "Activa tu cuenta")
        self.assertContains(response, "/activate/")
