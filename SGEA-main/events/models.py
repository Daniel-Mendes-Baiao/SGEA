from django.db import models
from django.contrib.auth.models import User

# Evento com os campos pedidos: tipo, datas, horário, local, capacidade e organizador.
class Event(models.Model):
    EVENT_TYPES = (('seminario','Seminário'),('palestra','Palestra'),('minicurso','Minicurso'),('semana','Semana Acadêmica'))
    title = models.CharField('Título', max_length=200)
    event_type = models.CharField('Tipo', max_length=20, choices=EVENT_TYPES)
    start_date = models.DateField('Data inicial')
    end_date = models.DateField('Data final')
    time = models.CharField('Horário', max_length=50, help_text='Ex.: 14:00 - 18:00')
    place = models.CharField('Local', max_length=200)
    capacity = models.PositiveIntegerField('Capacidade')
    banner = models.ImageField('Banner', upload_to='events_banners/', blank=True, null=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events', verbose_name='Professor Responsável')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events', verbose_name='Criado por', null=True, blank=True)

    def __str__(self):
        return self.title
