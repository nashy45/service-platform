from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'user', 'amount', 'gateway', 'status', 'paid_at']
    list_filter = ['status', 'gateway']
    search_fields = ['user__email', 'transaction_id']
    readonly_fields = ['created_at']
