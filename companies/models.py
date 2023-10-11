from django.db import models
from companies.mixins import CompanyRequestProfileMixin, TimeStampMixin


class Company(TimeStampMixin, CompanyRequestProfileMixin):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_file = models.FileField(upload_to="company_profiles/")

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
