from django.contrib import admin
from companies.models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "address"]


admin.site.register(Company, CompanyAdmin)
