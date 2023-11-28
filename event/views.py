from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Event


# Create your views here.
class EvenViewSets(ModelViewSet):
    queryset = Event.objects.filter(status=True)
