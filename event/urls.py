from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvenViewSets

app_name = "event"

router = DefaultRouter()
router.register('event', EvenViewSets, basename='event')

urlpatterns = [
    path("", include(router.urls)),
]