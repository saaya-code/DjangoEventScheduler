from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event-list'),
    path('create/', views.EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('<int:pk>/edit/', views.EventUpdateView.as_view(), name='event-edit'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event-delete'),
    path('<int:pk>/register/', views.EventRegistrationView.as_view(), name='event-register'),
    path('<int:pk>/cancel/<int:attendee_id>/', views.CancelRegistrationView.as_view(), name='registration-cancel'),
    path('category/<int:pk>/', views.CategoryEventListView.as_view(), name='category-events'),
    path('my-events/', views.UserEventListView.as_view(), name='user-events'),
    path('created-events/', views.CreatedEventsListView.as_view(), name='created-events'),
    path('joined-events/', views.JoinedEventsListView.as_view(), name='joined-events'),
]