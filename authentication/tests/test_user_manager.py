from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testpassword",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@test.com")
        self.assertIsNone(user.email_verified_on)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username="", email="testuser@test.com", password="foo"
            )
        with self.assertRaises(ValueError):
            User.objects.create_user(username="testuser", email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="super", email="super@test.com", password="testpassword"
        )
        self.assertEqual(admin_user.email, "super@test.com")
        self.assertIsNone(admin_user.email_verified_on)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username="super",
                email="super@user.com",
                password="foo",
                is_superuser=False,
            )
