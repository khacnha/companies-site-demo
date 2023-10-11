from django.db import models
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.exceptions import ObjectDoesNotExist


class TimeStampMixin(models.Model):
    """
    Timestamped Model Mixin
    Fields:
        created_at
        updated_at

    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CompanyRequestProfileMixin:
    """
    Mixin to handle company's profile request flow
    """

    def run_profile_request_flow(self, request):
        # params
        domain = get_current_site(request).domain
        protocol = "https" if request.is_secure() else "http"
        site_url = f"{protocol}://{domain}"
        requester = request.user

        # get superuser
        User = get_user_model()
        admins = User.super.all()
        for admin in admins:
            self.send_profile_request_mail_to_admin(requester, admin, site_url)

    def send_profile_request_mail_to_admin(self, requester, superuser, site_url):
        email_verification_path = reverse(
            "companies:approved-profile-request",
            kwargs={
                "cidb64": urlsafe_base64_encode(force_bytes(self.pk)),
                "uidb64": urlsafe_base64_encode(force_bytes(requester.pk)),
                "token": requester.generator_email_token(),
            },
        )
        mail_subject = f"Request permission to view {self}'s profiles!!"

        template_context = dict(
            superuser=superuser.username,
            company=self.name,
            requester=requester.username,
            email_verification_url=f"{site_url}{email_verification_path}",
        )
        html_string = render_to_string(
            "emails/request-company-profile.html", template_context
        )
        text_string = render_to_string(
            "emails/request-company-profile.txt",
            template_context,
        )

        return superuser.send_email(
            mail_subject,
            text_string,
            html_message=html_string,
        )

    def send_profile_to_user_email(self, user):
        profile_presigned = self.profile_file  # todo
        mail_subject = f"Company profile of {self} company!!"

        template_context = dict(
            user=user.username,
            company=self.name,
            download_link=profile_presigned,
        )
        html_string = render_to_string(
            "emails/download-company-profile.html", template_context
        )
        text_string = render_to_string(
            "emails/download-company-profile.txt",
            template_context,
        )

        return user.send_email(
            mail_subject,
            text_string,
            html_message=html_string,
        )

    @staticmethod
    def verify_approve_profile_request_token(cidb64, uidb64, token):
        User = get_user_model()
        try:
            company_id = force_str(urlsafe_base64_decode(cidb64))
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            return None

        if user is not None and user.check_email_token(token):
            return [company_id, user]
        else:
            return None
