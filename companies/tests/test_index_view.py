from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from companies.models import Company
from django.core import mail


class TestIndexView(TestCase):
    def test_index_page_unauthentication(self):
        response = self.client.get(reverse("companies:index"))

        self.assertEqual(response.status_code, 302)

    def test_index_page_authentication(self):
        # Login
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="password",
        )
        self.client.login(username=user.username, password="password")

        # Create Company data
        for company_id in range(10):
            Company.objects.create(
                name=f"company {company_id}",
                address=f"address {company_id}",
                profile_file=f"file{company_id}.pdf",
            )

        response = self.client.get(reverse("companies:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("page_obj", response.context)
        self.assertEqual(len(response.context["page_obj"]), 10)

    def test_profile_request_with_user_unverify_email(self):
        User = get_user_model()

        # user login
        user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="password",
        )
        self.client.login(username=user.username, password="password")

        # profile request
        company = Company.objects.create(
            name="company1",
            address="address1",
            profile_file="file.pdf",
        )

        response = self.client.post(
            reverse("companies:profile-request"),
            content_type="application/json",
            data={
                "company_id": company.pk,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_profile_request_success(self):
        User = get_user_model()

        # create superuser
        User.objects.create_superuser(
            username="superadmin",
            email="superadmin@test.com",
            password="password",
        )

        # user login
        user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="password",
            email_verified_on=timezone.now(),
        )
        self.client.login(username=user.username, password="password")

        # profile request
        company = Company.objects.create(
            name="company1",
            address="address1",
            profile_file="file.pdf",
        )

        response = self.client.post(
            reverse("companies:profile-request"),
            content_type="application/json",
            data={
                "company_id": company.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
