from django.urls import path
from .views import RegistrationView, LoginView, EventRegistrationAPIView, EventUnRegistrationAPIView

app_name = "users"

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/event-register/', EventRegistrationAPIView.as_view(), name='event-registration'),
    path('user/event-unregister/', EventUnRegistrationAPIView.as_view(), name='event-unregister'),
]
