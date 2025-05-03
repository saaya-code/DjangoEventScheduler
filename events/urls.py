from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event-list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('<int:pk>/register/', views.EventRegistrationView.as_view(), name='event-register'),
    path('<int:pk>/cancel/<int:attendee_id>/', views.CancelRegistrationView.as_view(), name='registration-cancel'),
    path('category/<int:pk>/', views.CategoryEventListView.as_view(), name='category-events'),
]