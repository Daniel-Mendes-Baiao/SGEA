from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from events.models import Event
from registrations.models import Registration
from certificates.models import Certificate
from .models import AuditLog
import inspect

def get_current_user():
    # Helper to get user from stack frame (hacky but works for signals without middleware)
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            return request.user
    return None

@receiver(post_save, sender=Event)
def log_event_save(sender, instance, created, **kwargs):
    user = get_current_user()
    action = 'CREATE_EVENT' if created else 'UPDATE_EVENT'
    AuditLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action=action,
        target_model='Event',
        target_id=instance.id,
        details=f'Evento: {instance.title}'
    )

@receiver(post_delete, sender=Event)
def log_event_delete(sender, instance, **kwargs):
    user = get_current_user()
    AuditLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action='DELETE_EVENT',
        target_model='Event',
        target_id=instance.id,
        details=f'Evento: {instance.title}'
    )

@receiver(post_save, sender=Registration)
def log_registration_save(sender, instance, created, **kwargs):
    if created:
        user = get_current_user()
        AuditLog.objects.create(
            user=user if user and user.is_authenticated else None,
            action='ENROLL',
            target_model='Registration',
            target_id=instance.id,
            details=f'Inscrição: {instance.user.username} em {instance.event.title}'
        )

@receiver(post_delete, sender=Registration)
def log_registration_delete(sender, instance, **kwargs):
    user = get_current_user()
    AuditLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action='CANCEL_ENROLL',
        target_model='Registration',
        target_id=instance.id,
        details=f'Cancelamento: {instance.user.username} em {instance.event.title}'
    )

@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    if created:
        user = get_current_user()
        # Only log if created by an organizer (not self-registration)
        if user and user.is_authenticated and user != instance:
            AuditLog.objects.create(
                user=user,
                action='CREATE_USER',
                target_model='User',
                target_id=instance.id,
                details=f'Usuário criado: {instance.username}'
            )

@receiver(post_save, sender=Certificate)
def log_certificate_generation(sender, instance, created, **kwargs):
    if created:
        user = get_current_user()
        AuditLog.objects.create(
            user=user if user and user.is_authenticated else None,
            action='GENERATE_CERTIFICATE',
            target_model='Certificate',
            target_id=instance.id,
            details=f'Certificado gerado para: {instance.registration.user.username} - {instance.registration.event.title}'
        )

