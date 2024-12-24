from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Client


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client


@admin.register(Client)
class ClientAdmin(UserAdmin):
    """
    Admin configuration for the Client model.
    """
    model = Client
    list_display = ('email', 'first_name', 'last_name', 'provider', 'is_staff', 'is_active', 'date_joined', 'main_character')
    list_filter = ('provider', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('date_joined',)

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'main_character')
        }),
        ('Provider Info', {
            'fields': ('provider',)
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'provider', 'is_staff', 'is_active'),
        }),
    )

