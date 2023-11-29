from rest_framework.serializers import ModelSerializer
from .models import Event


class EventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'available_slot', 'status', 'location']
