from django.db import models
from django.urls import reverse

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
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})


class Attendee(models.Model):
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
