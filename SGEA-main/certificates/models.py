from django.db import models
from registrations.models import Registration

class Certificate(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f"Certificado {self.code}"
