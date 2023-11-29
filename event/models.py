from django.db import models


class Keywords(models.Model):
    name = models.CharField(max_length=255)

    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Keywords"
        verbose_name_plural = "Keywords"


# Create your models here.
class Event(models.Model):
    keywords = models.ManyToManyField(Keywords, related_name='event_keywords')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    available_slot = models.IntegerField(default=0)

    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
