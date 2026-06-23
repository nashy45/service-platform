from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'provider', 'service', 'booking_date', 'status', 'total_price']
    list_filter = ['status', 'booking_date']
    search_fields = ['customer__email', 'provider__user__email']
    readonly_fields = ['created_at', 'updated_at']
