from django.urls import path
from . import views

urlpatterns = [
    path('my/', views.my_certificates, name='my_certificates'),
    path('issue/<int:registration_id>/', views.issue, name='issue_certificate'),
    path('download/<int:certificate_id>/', views.download, name='download_certificate'),
]
