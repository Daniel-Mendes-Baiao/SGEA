from django.urls import path
from . import views

urlpatterns = [
    path('event/<int:event_id>/', views.event_registrations, name='report_event_regs'),
    path('event/<int:event_id>/csv/', views.event_registrations_csv, name='report_event_regs_csv'),
    path('event/<int:event_id>/pdf/', views.event_registrations_pdf, name='report_event_regs_pdf'),
]
