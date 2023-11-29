from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSets, SearchEventApiView

app_name = "event"

router = DefaultRouter()
router.register('event', EventViewSets, basename='event')

urlpatterns = [
    path('search/event', SearchEventApiView.as_view(), name='registration'),
    path("", include(router.urls)),
]
