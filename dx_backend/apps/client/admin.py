from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Client


@admin.register(Client)
class ClientAdmin(UserAdmin):
    """
    Admin configuration for the Client model.
    """
    model = Client
    list_display = ('email', 'first_name', 'last_name', 'provider', 'is_staff', 'is_active', 'date_joined',
                    'main_character', 'current_campaign', 'get_characters_count', 'view_characters')
    list_filter = ('provider', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('date_joined',)

    def get_characters_count(self, obj):
        """Get the number of characters owned by this client"""
        return obj.available_characters.count()

    get_characters_count.short_description = 'Characters'

    def view_characters(self, obj):
        """Button to view characters owned by this client"""
        return format_html(
            '<a class="button" style="display: inline-block; padding: 6px 10px; margin: 0 2px; '
            'background: #007bff; color: white; border: none; border-radius: 4px; '
            'text-decoration: none; font-size: 12px; font-weight: bold; '
            'box-shadow: 0 1px 3px rgba(0,0,0,0.2); white-space: nowrap; overflow: visible;" href="{}">'
            '<span style="margin-right: 4px;">👥</span>Characters</a>',
            f"/admin/character/character/?owner__id__exact={obj.pk}"
        )

    view_characters.short_description = 'View Characters'

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'main_character', 'current_campaign')
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

    filter_horizontal = ('groups', 'user_permissions')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'provider', 'is_staff', 'is_active'),
        }),
    )
