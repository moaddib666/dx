from django.contrib import admin
from django.utils.safestring import mark_safe  # Import mark_safe to render HTML safely

from .models import Effect, ActiveEffect


@admin.register(Effect)
class EffectAdmin(admin.ModelAdmin):
    list_display = ('id', 'icon_preview', 'permanent', 'ends_in')
    list_filter = ('permanent',)  # Allows filtering by permanence
    search_fields = ('id',)  # Enables searching by Effect ID
    ordering = ('id',)
    readonly_fields = ('icon_preview',)
    fields = ('id', 'icon', 'icon_preview', 'permanent', 'ends_in')  # Fields to display in the form

    def icon_preview(self, obj):
        if obj.icon:
            return mark_safe(f'<img src="{obj.icon.url}" style="max-height: 50px; max-width: 50px;" />')
        return "No Icon"

    icon_preview.short_description = "Icon Preview"


@admin.register(ActiveEffect)
class ActiveEffectAdmin(admin.ModelAdmin):
    list_display = ('effect', 'target', 'duration', 'active', 'impact_preview')
    list_filter = ('active', 'effect')  # Enables filtering by active state and effect
    search_fields = ('target__name', 'effect__id')  # Search by target name and effect ID
    ordering = ('-duration',)  # Orders by duration descending
    fields = ('effect', 'target', 'duration', 'active', 'impact', '_data')  # Fields to display in the form
    readonly_fields = ('impact_preview',)

    def impact_preview(self, obj):
        if obj.impact:
            return mark_safe(f'<pre>{obj.impact}</pre>')
        return "No Impact Data"

    impact_preview.short_description = "Impact Preview"
