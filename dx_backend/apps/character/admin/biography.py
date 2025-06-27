from django.contrib import admin
from django.utils.html import format_html

from apps.core.admin import CampaignModelAdmin
from ..models import CharacterBiography


@admin.register(CharacterBiography)
class CharacterBiographyAdmin(CampaignModelAdmin):
    """
    Admin interface for CharacterBiography.
    """
    list_display = ('character', 'age', 'gender', 'background', 'avatar_preview')
    search_fields = ('character__name', 'background', 'appearance')
    readonly_fields = ('avatar_preview',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        campaign_id = request.session.get('campaign_id')
        if campaign_id:
            return qs.filter(character__campaign_id=campaign_id)
        return qs

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.avatar.url)
        return "No Image"

    avatar_preview.short_description = "Avatar Preview"
