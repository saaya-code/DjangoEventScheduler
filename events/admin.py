from django.contrib import admin
from .models import EventCategory, Event, Attendee, Registration

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'category')
    list_filter = ('category', 'date')
    search_fields = ('title', 'location')
    date_hierarchy = 'date'

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'event', 'registered_on')
    list_filter = ('event', 'registered_on')
    search_fields = ('attendee__name', 'attendee__email', 'event__title')
    date_hierarchy = 'registered_on'
