from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvenViewSets, SearchEventApiView

app_name = "event"

router = DefaultRouter()
router.register('event', EvenViewSets, basename='event')

urlpatterns = [
    path('event/search', SearchEventApiView.as_view(), name='registration'),
    path("", include(router.urls)),
]
