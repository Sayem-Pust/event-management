from django.db import models
from django.contrib.auth import get_user_model
from event.models import Event
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


# Create your models here.
class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_details_event')
    event = models.ManyToManyField(Event, related_name='event_details')

    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserEvent.objects.create(user=instance)
