from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from .models import Event, Keywords
from .serializers import EventSerializer
from django.db.models import Q


# Create your views here.
class EventViewSets(ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Event.objects.filter(status=True)
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['create', 'delete', 'update']:
            self.permission_classes = [IsAuthenticated]
        return super(EventViewSets, self).get_permissions()

    def perform_update(self, serializer):
        keywords_data = self.request.data.get('keywords', [])

        instance = serializer.save()

        instance.keywords.set(Keywords.objects.filter(id__in=keywords_data))

    def create(self, request, *args, **kwargs):
        keywords_data = request.data.getlist('keywords')

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            event_instance = serializer.instance
            event_instance.keywords.set(Keywords.objects.filter(id__in=keywords_data))

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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
