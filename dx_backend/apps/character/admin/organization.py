from django.contrib import admin
from django.utils.html import format_html
from apps.core.admin import CampaignModelAdmin

from ..models import Organization


@admin.register(Organization)
class OrganizationAdmin(CampaignModelAdmin):
    list_display = ('name', 'behavior_badge', 'description_short')
    list_filter = ('behavior',)
    search_fields = ('name', 'description')
    list_per_page = 25
    ordering = ('name',)

    def behavior_badge(self, obj):
        """Display behavior as a colored badge"""
        colors = {
            'PASSIVE': '#28a745',  # Green
            'NEUTRAL': '#6c757d',  # Gray
            'AGGRESSIVE': '#dc3545',  # Red
            'FRIENDLY': '#17a2b8',  # Blue
            'HOSTILE': '#fd7e14',  # Orange
        }
        color = colors.get(obj.behavior, '#6c757d')

        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 10px; font-size: 0.8em;">{}</span>',
            color, obj.behavior
        )

    behavior_badge.short_description = "Behavior"
    behavior_badge.admin_order_field = 'behavior'

    def description_short(self, obj):
        """Display a shortened version of the description"""
        if len(obj.description) > 100:
            return obj.description[:97] + '...'
        return obj.description

    description_short.short_description = "Description"
