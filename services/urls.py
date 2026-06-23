from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.category_list, name='category_list'),
    path('services/<slug:slug>/', views.category_detail, name='category_detail'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('providers/', views.provider_list, name='provider_list'),
    path('providers/<int:pk>/', views.provider_detail, name='provider_detail'),
    # Provider service management
    path('my-services/', views.my_services, name='my_services'),
    path('my-services/add/', views.add_service, name='add_service'),
    path('my-services/<int:pk>/edit/', views.edit_service, name='edit_service'),
    path('my-services/<int:pk>/delete/', views.delete_service, name='delete_service'),
]
