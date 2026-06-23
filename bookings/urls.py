from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:service_id>/', views.create_booking, name='create_booking'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:pk>/status/<str:status>/', views.update_booking_status, name='update_booking_status'),
]
