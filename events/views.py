from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden

from .models import Event, EventCategory, Attendee, Registration
from .forms import EventForm
from django.views import View

# Custom mixin to verify that the user is the creator of an event
class UserIsEventCreatorMixin(UserPassesTestMixin):
    def test_func(self):
        event = self.get_object()
        return self.request.user == event.creator
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit or delete this event.")
        return redirect('event-detail', pk=self.get_object().pk)

# New view for showing events created by the user
class CreatedEventsListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/created_events.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user).order_by('date')

# New view for showing events the user has joined (registered for)
class JoinedEventsListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/joined_events.html'
    context_object_name = 'registrations'
    
    def get_queryset(self):
        # Try to get the attendee associated with the user
        try:
            attendee = Attendee.objects.get(user=self.request.user)
            return Registration.objects.filter(attendee=attendee).order_by('event__date')
        except Attendee.DoesNotExist:
            return Registration.objects.none()

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
        
        # Add user registration directly if user is authenticated
        if self.request.user.is_authenticated:
            try:
                user_registration = Registration.objects.filter(
                    event=self.object,
                    attendee__user=self.request.user
                ).first()
                context['user_registration'] = user_registration
            except:
                context['user_registration'] = None
                
        return context


class EventRegistrationView(View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        
        # If user is authenticated, use their information
        if request.user.is_authenticated:
            name = request.user.get_full_name() or request.user.username
            email = request.user.email
            
            # Get or create attendee linked to user
            attendee, created = Attendee.objects.get_or_create(
                user=request.user,
                defaults={'name': name, 'email': email}
            )
        else:
            name = request.POST.get('name')
            email = request.POST.get('email')
            
            if not name or not email:
                messages.error(request, 'Both name and email are required.')
                return redirect('event-detail', pk=event.pk)
            
            # Get or create attendee without user link
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


class UserEventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/user_events.html'
    context_object_name = 'registrations'
    
    def get_queryset(self):
        # Try to get the attendee associated with the user
        try:
            attendee = Attendee.objects.get(user=self.request.user)
            return Registration.objects.filter(attendee=attendee).order_by('event__date')
        except Attendee.DoesNotExist:
            return Registration.objects.none()


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    
    def get_success_url(self):
        return reverse('event-detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, 'Your event has been created successfully!')
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserIsEventCreatorMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Your event has been updated successfully!')
        return reverse('event-detail', kwargs={'pk': self.object.pk})


class EventDeleteView(LoginRequiredMixin, UserIsEventCreatorMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('event-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your event has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
