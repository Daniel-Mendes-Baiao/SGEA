from django.urls import path
from . import views
urlpatterns = [
    path('enroll/<int:event_id>/', views.enroll, name='enroll'),
    path('cancel/<int:event_id>/', views.cancel_enrollment, name='cancel_enrollment'),
    path('attendance/<int:event_id>/', views.manage_attendance, name='manage_attendance'),
]
