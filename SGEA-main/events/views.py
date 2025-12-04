from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Event
from .forms import EventForm
from registrations.models import Registration


def _role(user):
    return getattr(getattr(user, 'profile', None), 'role', None)


def event_list(request):
    events = Event.objects.all().order_by('start_date')
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    already_registered = False
    user_certificate = None
    
    if request.user.is_authenticated:
        from registrations.models import Registration
        from certificates.models import Certificate
        
        already_registered = Registration.objects.filter(user=request.user, event=event).exists()
        
        # Check if user has a certificate for this event
        try:
            registration = Registration.objects.get(user=request.user, event=event)
            user_certificate = Certificate.objects.get(registration=registration)
        except (Registration.DoesNotExist, Certificate.DoesNotExist):
            pass
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'already_registered': already_registered,
        'user_certificate': user_certificate
    })


@login_required
def event_create(request):
    # só organizador pode criar
    if _role(request.user) != 'organizador':
        messages.error(request, 'Apenas organizadores podem criar eventos.')
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.creator = request.user  # Salva quem criou o evento
            ev.save()
            messages.success(request, 'Evento criado com sucesso.')
            return redirect('event_detail', event_id=ev.id)
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {'form': form})
