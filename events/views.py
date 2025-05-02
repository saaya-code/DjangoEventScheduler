from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db import IntegrityError

from .models import Event, EventCategory, Attendee, Registration
from django.views import View

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset.order_by('date')


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registrations'] = Registration.objects.filter(event=self.object)
        return context


class EventRegistrationView(View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        if not name or not email:
            messages.error(request, 'Both name and email are required.')
            return redirect('event-detail', pk=event.pk)
        
        # Get or create attendee
        attendee, created = Attendee.objects.get_or_create(
            email=email,
            defaults={'name': name}
        )
        
        # If attendee exists but with different name, update it
        if not created and attendee.name != name:
            attendee.name = name
            attendee.save()
        
        try:
            Registration.objects.create(attendee=attendee, event=event)
            messages.success(request, f'You have successfully registered for {event.title}!')
        except IntegrityError:
            messages.error(request, 'You are already registered for this event.')
        
        return redirect('event-detail', pk=event.pk)


class CancelRegistrationView(View):
    def post(self, request, pk, attendee_id):
        event = get_object_or_404(Event, pk=pk)
        attendee = get_object_or_404(Attendee, pk=attendee_id)
        
        try:
            registration = Registration.objects.get(event=event, attendee=attendee)
            registration.delete()
            messages.success(request, f'Your registration for {event.title} has been canceled.')
        except Registration.DoesNotExist:
            messages.error(request, 'Registration not found.')
        
        return redirect('event-detail', pk=event.pk)


class CategoryEventListView(ListView):
    model = Event
    template_name = 'events/category_event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        self.category = get_object_or_404(EventCategory, pk=self.kwargs['pk'])
        return Event.objects.filter(category=self.category).order_by('date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
