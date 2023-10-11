from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from authentication.managers import UserManager
from authentication.mixins import UserEmailMixin


class User(AbstractUser, UserEmailMixin):
    """
    User Model
    """

    email = models.EmailField(_("email address"), unique=True)
    email_verified_on = models.DateTimeField(
        _("email verified on"), blank=True, null=True
    )

    objects = UserManager()

    @property
    def email_verified(self):
        """check email verified property"""
        return self.email and self.email_verified_on is not None
