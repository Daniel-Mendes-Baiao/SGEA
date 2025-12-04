from django.contrib import admin
from .models import Event
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=('title','event_type','start_date','end_date','place','capacity','organizer')
    list_filter=('event_type','start_date')
    search_fields=('title','place')
