from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from events.models import Event
from .models import Registration
import secrets
from certificates.models import Certificate

def _role(user):
    return getattr(getattr(user, 'profile', None), 'role', None)

@login_required
def enroll(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if Registration.objects.filter(user=request.user, event=event).exists():
        messages.info(request, 'Você já está inscrito neste evento.')
        return redirect('event_detail', event_id=event.id)
    
    if Registration.objects.filter(event=event).count() >= event.capacity:
        messages.error(request, 'Evento lotado.')
        return redirect('event_detail', event_id=event.id)
    
    Registration.objects.create(user=request.user, event=event)
    messages.success(request, 'Inscrição realizada com sucesso!')
    return redirect('event_detail', event_id=event.id)

@login_required
def cancel_enrollment(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    # Check if user is registered
    registration = get_object_or_404(Registration, user=request.user, event=event)
    
    # Check if event has already started (optional rule, but good practice)
    from django.utils import timezone
    if event.start_date < timezone.now().date():
        messages.error(request, 'Não é possível cancelar inscrição de um evento que já iniciou.')
        return redirect('event_detail', event_id=event.id)
        
    if request.method == 'POST':
        registration.delete()
        messages.success(request, 'Inscrição cancelada com sucesso.')
        return redirect('event_detail', event_id=event.id)
        
    return render(request, 'registrations/confirm_cancellation.html', {'event': event})

@login_required
def manage_attendance(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    # Only the creator (organizador who created the event) can manage attendance
    if event.creator != request.user:
        messages.error(request, 'Apenas o organizador que criou este evento pode gerenciar presenças.')
        return redirect('event_detail', event_id=event.id)
    
    registrations = Registration.objects.filter(event=event).select_related('user')
    
    if request.method == 'POST':
        # Get list of user IDs that attended
        attended_ids = request.POST.getlist('attended')
        
        # Update all registrations
        for reg in registrations:
            reg.attended = str(reg.id) in attended_ids
            reg.save()
        
        # Auto-generate certificates for attended users
        for reg in registrations.filter(attended=True):
            if not hasattr(reg, 'certificate'):
                Certificate.objects.create(
                    registration=reg,
                    code=secrets.token_hex(8)
                )
        
        messages.success(request, 'Presenças atualizadas e certificados gerados!')
        return redirect('event_detail', event_id=event.id)
    
    return render(request, 'registrations/manage_attendance.html', {
        'event': event,
        'registrations': registrations
    })
