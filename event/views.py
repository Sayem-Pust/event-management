from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import EventSerializer
from .models import Event
from django.db.models import Q


# Create your views here.
class EvenViewSets(ModelViewSet):
    queryset = Event.objects.filter(status=True)


class SearchEventApiView(APIView):

    def get(self, request):
        search_params = request.query_params.get('search_params', '')
        qs = Event.objects.filter(Q(title__icontains=search_params) |
                                  Q(keywords__name__icontains=search_params) |
                                  Q(description__icontains=search_params)).distinct()
        serializer = EventSerializer(qs, many=True)
        return Response({
            "data": serializer.data,
            "message": "Data get successfully"
        })
