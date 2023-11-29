from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Event, Keywords


class KeywordsSerializer(ModelSerializer):
    class Meta:
        model = Keywords
        fields = ['id', 'name']


class EventSerializer(ModelSerializer):
    # keywords = KeywordsSerializer(many=True)
    keywords = KeywordsSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'available_slot',
                  'location', 'keywords']
