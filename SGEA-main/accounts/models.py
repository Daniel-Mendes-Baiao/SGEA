from django.db import models
from django.contrib.auth.models import User
import uuid

# Perfil simples ligado ao User padrão do Django.
# Campos pedidos pelo enunciado: telefone, instituição (obrigatório p/ aluno e professor), perfil (role).
class Profile(models.Model):
    ROLE_CHOICES = (('aluno','Aluno'),('professor','Professor'),('organizador','Organizador'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField('Telefone', max_length=20, blank=True)
    institution = models.CharField('Instituição', max_length=200, blank=True)  # validado no form p/ perfis aluno/professor
    role = models.CharField('Perfil', max_length=20, choices=ROLE_CHOICES, default='aluno')
    email_confirmed = models.BooleanField('Email Confirmado', default=False)
    confirmation_token = models.CharField('Token de Confirmação', max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    
    def generate_confirmation_token(self):
        self.confirmation_token = str(uuid.uuid4())
        self.save()
        return self.confirmation_token
