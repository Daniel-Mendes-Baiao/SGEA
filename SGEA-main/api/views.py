from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from events.models import Event
from registrations.models import Registration
from audit.models import AuditLog

class EventsThrottle(UserRateThrottle):
    scope = 'events'

class EnrollmentsThrottle(UserRateThrottle):
    scope = 'enrollments'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([EventsThrottle])
def list_events(request):
    # Log API query
    AuditLog.objects.create(
        user=request.user,
        action='API_QUERY_EVENTS',
        target_model='Event',
        details=f'Consulta de eventos via API por {request.user.username}'
    )
    
    events = Event.objects.all()
    data = []
    for event in events:
        data.append({
            'id': event.id,
            'title': event.title,
            'event_type': event.get_event_type_display(),
            'start_date': event.start_date,
            'end_date': event.end_date,
            'place': event.place,
            'capacity': event.capacity,
            'organizer': event.organizer.username
        })
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([EnrollmentsThrottle])
def enroll_event(request):
    event_id = request.data.get('event_id')
    if not event_id:
        return Response({'error': 'event_id é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Log API enrollment attempt
    AuditLog.objects.create(
        user=request.user,
        action='API_ENROLL_ATTEMPT',
        target_model='Event',
        target_id=event_id,
        details=f'Tentativa de inscrição via API no evento {event_id} por {request.user.username}'
    )
    
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Evento não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    if Registration.objects.filter(user=request.user, event=event).exists():
        return Response({'error': 'Você já está inscrito neste evento'}, status=status.HTTP_400_BAD_REQUEST)
    
    if Registration.objects.filter(event=event).count() >= event.capacity:
        return Response({'error': 'Evento lotado'}, status=status.HTTP_400_BAD_REQUEST)
    
    Registration.objects.create(user=request.user, event=event)
    return Response({'message': 'Inscrição realizada com sucesso'}, status=status.HTTP_201_CREATED)
