from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('registration', 'code', 'issued_at')
    search_fields = ('code', 'registration__user__username', 'registration__event__title')
