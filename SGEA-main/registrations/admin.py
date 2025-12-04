from django.contrib import admin
from .models import Registration
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display=('user','event','created_at')
    list_filter=('created_at',)
    search_fields=('user__username','event__title')
