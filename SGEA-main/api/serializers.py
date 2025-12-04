from rest_framework import serializers
from events.models import Event
from registrations.models import Registration


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'event_type', 'start_date', 'end_date', 'place', 'organizer']


class EnrollmentSerializer(serializers.Serializer):
    event_id = serializers.IntegerField()
    
    def validate_event_id(self, value):
        try:
            Event.objects.get(id=value)
        except Event.DoesNotExist:
            raise serializers.ValidationError("Event not found.")
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        event = Event.objects.get(id=validated_data['event_id'])
        
        # Check if already enrolled
        if Registration.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("Already enrolled in this event.")
        
        # Check capacity
        count = Registration.objects.filter(event=event).count()
        if count >= event.capacity:
            raise serializers.ValidationError("Event is at full capacity.")
        
        registration = Registration.objects.create(user=user, event=event)
        return registration
