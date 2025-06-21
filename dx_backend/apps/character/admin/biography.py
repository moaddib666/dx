from django.contrib import admin
from django.utils.html import format_html

from ..models import CharacterBiography


@admin.register(CharacterBiography)
class CharacterBiographyAdmin(admin.ModelAdmin):
    """
    Admin interface for CharacterBiography.
    """
    list_display = ('character', 'age', 'gender', 'background', 'avatar_preview')
    search_fields = ('character__name', 'background', 'appearance')
    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.avatar.url)
        return "No Image"

    avatar_preview.short_description = "Avatar Preview"