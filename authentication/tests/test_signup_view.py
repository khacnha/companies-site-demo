from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core import mail


class TestSignUpView(TestCase):
    def test_get_sign_up(self):
        response = self.client.get(reverse("authentication:signup"))

        self.assertEqual(response.status_code, 200)

    def test_post_sign_up_success(self):
        User = get_user_model()
        response = self.client.post(
            reverse("authentication:signup"),
            data={
                "username": "testuser",
                "email": "testuser@test.com",
                "password1": "Abc@123123",
                "password2": "Abc@123123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_post_sign_up_validate(self):
        User = get_user_model()
        User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="password",
        )
        response = self.client.post(
            reverse("authentication:signup"),
            data={
                "username": "testuser",
                "email": "testuser@test.com",
                "password1": "Abc@123123",
                "password2": "Abc@123123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context["form"])
