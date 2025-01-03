from django.contrib import admin
from django.utils.html import format_html
from .models import Shield, ActiveShield


@admin.register(Shield)
class ShieldAdmin(admin.ModelAdmin):
    """Admin configuration for Shield model."""
    list_display = ('id', 'icon_preview', 'base_health', 'base_efficiency')
    search_fields = ('id',)
    list_filter = ('id',)
    fields = ('id', 'icon', 'icon_preview', 'base_health', 'base_efficiency')
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        """Display shield icon as a thumbnail in the admin panel."""
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.icon.url)
        return "No Icon"

    icon_preview.short_description = "Icon Preview"


@admin.register(ActiveShield)
class ActiveShieldAdmin(admin.ModelAdmin):
    """Admin configuration for ActiveShield model."""
    list_display = ('shield', 'target', 'level', 'health', 'efficiency', 'cycles_left')
    list_filter = ('shield', 'cycles_left')
    search_fields = ('shield__id', 'target__name')
    fields = ('shield', 'target', 'level', 'health', 'efficiency', 'cycles_left', 'icon_preview')
    readonly_fields = ('icon_preview', )

    def icon_preview(self, obj):
        """Display the associated shield's icon in the admin panel."""
        if obj.shield and obj.shield.icon:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.shield.icon.url)
        return "No Icon"

    icon_preview.short_description = "Shield Icon Preview"
