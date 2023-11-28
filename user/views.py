from django.contrib.auth.models import User
from .serializers import RegistrationSerializer
from rest_framework import generics, permissions, views
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, response
from .models import UserEvent
from event.views import Event
from datetime import datetime


class RegistrationView(generics.CreateAPIView):
    """ User Registration with username, email, first name, last name, password, confirm password and
     is superuser(optional) on the top of django build in authentication system """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer


class LoginView(generics.CreateAPIView):
    """ User Login with username or email and password and get a access token for authentication"""
    queryset = User.objects.filter(is_active=True)

    def post(self, request):
        password = request.data.get('password')
        identifier = request.data.get('identifier')
        user_instance = User.objects.filter(
            Q(email=identifier) | Q(username=identifier)).first()
        if user_instance is not None:
            if user_instance.check_password(password):
                refresh = RefreshToken.for_user(user_instance)
                return response.Response(
                    {
                        'message': 'login successful',
                        'data': {
                            'user': RegistrationSerializer(user_instance).data,
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return response.Response(
                    {
                        'message': 'Invalid Credential',
                        'is_active': True
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return response.Response(
                {
                    'message': 'Invalid Credential',
                    'is_active': True
                }, status=status.HTTP_400_BAD_REQUEST
            )


class EventRegistrationAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        event_data = request.data.get('event')
        qs_ex = UserEvent.objects.filter(user=request.user, event=event_data)
        if qs_ex.exists():
            return response.Response({'error': 'User already register for this event'}
                                     , status=status.HTTP_400_BAD_REQUEST)
        else:
            qs = UserEvent.objects.get(user=request.user)
            event = Event.objects.filter(id=event_data, status=True)
            if event.exists():
                event = event.first()
                if event.available_slot == 0:
                    return response.Response({'error': 'Sorry, There is no available slot for you'}
                                             , status=status.HTTP_400_BAD_REQUEST)
                event_datetime = datetime.combine(event.date, event.time)
                if event_datetime < datetime.now():
                    return response.Response({'error': 'Event has already passed'}, status=status.HTTP_400_BAD_REQUEST)

                qs.event.add(event_data)
                qs.save()
                event.available_slot -= 1
                event.save()
                return response.Response({
                    "message": "User registered successfully"
                })
            return response.Response({
                "message": "Event expired or not found"
            })


class EventUnRegistrationAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        event_data = request.data.get('event')
        qs_ex = UserEvent.objects.filter(user=request.user, event=event_data)
        if qs_ex.exists():
            qs_ex = qs_ex.first()
            event = Event.objects.get(id=event_data, status=True)
            event_datetime = datetime.combine(event.date, event.time)
            if event_datetime < datetime.now():
                return response.Response({'error': 'Event has already passed'}, status=status.HTTP_400_BAD_REQUEST)
            event.available_slot += 1
            qs_ex.event.remove(event_data)
            qs_ex.save()
            event.save()
            return response.Response({
                "message": "User Unregistered successfully"
            })
        return response.Response({
            "message": "User not registered for this event"
        })
