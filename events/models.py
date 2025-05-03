from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Event Categories"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(EventCategory, related_name='events', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='created_events', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})


class Attendee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='attendee')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.name} ({self.email})"


class Registration(models.Model):
    attendee = models.ForeignKey(Attendee, related_name='registrations', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='registrations', on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['attendee', 'event']
        
    def __str__(self):
        return f"{self.attendee.name} - {self.event.title}"
