from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from authentication.tokens import email_verification_token
from django.contrib.auth import get_user_model


class UserEmailMixin:
    """
    Mixin for handling sending emails to user and the email verification bits
    """

    def send_email(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        from_email = from_email or settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def verify_email(self):
        self.email_verified_on = timezone.now()
        self.save()

    def generator_email_token(self):
        return email_verification_token.make_token(user=self)

    @staticmethod
    def verify_email_token(uidb64, token):
        User = get_user_model()
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

        if user is not None and email_verification_token.check_token(user, token):
            user.verify_email()
        else:
            return None
        return user

    def send_email_verification_email(self, request):
        domain = get_current_site(request).domain
        protocol = "https" if request.is_secure() else "http"

        email_verification_path = reverse(
            "authentication:email-verification",
            kwargs={
                "uidb64": urlsafe_base64_encode(force_bytes(self.pk)),
                "token": self.generator_email_token(),
            },
        )
        mail_subject = "Welcome to Our website!!"

        template_context = dict(
            user=self.username,
            email_verification_url=f"{protocol}://{domain}{email_verification_path}",
        )
        html_string = render_to_string(
            "emails/mail-verification.html", template_context
        )
        text_string = render_to_string(
            "emails/mail-verification.txt",
            template_context,
        )

        return self.send_email(
            mail_subject,
            text_string,
            html_message=html_string,
        )
