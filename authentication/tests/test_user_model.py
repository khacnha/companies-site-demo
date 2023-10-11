from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

User = get_user_model()


class TestUserModel(TestCase):
    def test_email_verified_true(self):
        user = User.objects.create_user(
            username="testuer",
            email="testuser@test.com",
            password="testpassword",
            email_verified_on=timezone.now(),
        )
        assert user.email_verified is True

    def test_email_verified_false(self):
        user = User.objects.create_user(
            username="testuer",
            email="testuser@test.com",
            password="testpassword",
        )
        assert user.email_verified is False
