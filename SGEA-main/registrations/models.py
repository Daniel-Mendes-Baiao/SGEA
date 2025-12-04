from django.db import models
from django.contrib.auth.models import User
from events.models import Event

# Inscrição simples: impede duplicidade por (user,event)
class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField('Presença Confirmada', default=False)

    class Meta:
        unique_together = ('user','event')

    def __str__(self):
        return f"{self.user} -> {self.event}"
