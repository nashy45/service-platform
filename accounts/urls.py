from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/provider/', views.register_provider, name='register_provider'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    # Password Reset (no email)
    path('reset-password/', views.reset_password_request, name='reset_password_request'),
    path('reset-password/set/<int:user_id>/', views.reset_password_set, name='reset_password_set'),
    # Provider availability toggle
    path('toggle-availability/', views.toggle_availability, name='toggle_availability'),
    # Admin
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/providers/', views.admin_providers, name='admin_providers'),
    path('admin-panel/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin-panel/providers/<int:pk>/<str:status>/', views.admin_approve_provider, name='admin_approve_provider'),
]
