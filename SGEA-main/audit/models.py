from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Usuário')
    action = models.CharField('Ação', max_length=50)
    target_model = models.CharField('Modelo Alvo', max_length=50)
    target_id = models.IntegerField('ID do Alvo', null=True, blank=True)
    details = models.TextField('Detalhes', blank=True)
    timestamp = models.DateTimeField('Data/Hora', auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
