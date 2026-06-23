from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ProviderProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'role', 'phone', 'is_active', 'created_at']
    list_filter = ['role', 'is_active']
    search_fields = ['email', 'username', 'phone']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Contact', {'fields': ('role', 'phone', 'profile_picture', 'address')}),
    )


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'rating', 'total_jobs', 'is_available', 'created_at']
    list_filter = ['status', 'is_available']
    search_fields = ['user__email']
    actions = ['approve_providers', 'reject_providers']

    def approve_providers(self, request, queryset):
        queryset.update(status='approved')
    approve_providers.short_description = 'Approve selected providers'

    def reject_providers(self, request, queryset):
        queryset.update(status='rejected')
    reject_providers.short_description = 'Reject selected providers'
