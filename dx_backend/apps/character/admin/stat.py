from django.contrib import admin

from ..models import Stat


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    """
    Admin interface for Stats management.
    """
    list_display = ('name', 'value', 'character')
    list_filter = ('name',)
    search_fields = ('character__name',)