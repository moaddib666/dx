from django.contrib import admin

from .models import Campaign, Session


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    """
    Admin interface for Campaign model.
    """
    list_display = ('name', 'description', 'is_active', 'is_completed')
    list_filter = ('is_active', 'is_completed')
    search_fields = ('name', 'description')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """
    Admin interface for Session model.
    """
    list_display = ('client', 'character')
    list_filter = ('client',)
    search_fields = ('client__name', 'character__name')
