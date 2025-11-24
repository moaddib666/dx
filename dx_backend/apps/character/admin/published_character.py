from django.contrib import admin
from django.utils.html import format_html

from apps.core.admin import CampaignModelAdmin
from ..models import PublishedCharacter


@admin.register(PublishedCharacter)
class PublishedCharacterAdmin(CampaignModelAdmin):
    """
    Admin interface for PublishedCharacter.
    """
    list_display = ('id', 'character_name', 'big_avatar_preview', 'small_avatar_preview', 'created_at', 'updated_at')
    search_fields = ('biography__character__name', 'biography__background', 'biography__appearance')
    readonly_fields = ('big_avatar_preview', 'small_avatar_preview', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('biography',)
    
    fieldsets = (
        ('Character Information', {
            'fields': ('biography',)
        }),
        ('Avatars', {
            'fields': ('big_avatar', 'big_avatar_preview', 'small_avatar', 'small_avatar_preview')
        }),
        ('Social Media Links', {
            'fields': ('tiktok_link', 'youtube_link', 'instagram_link')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def character_name(self, obj):
        """Display the character name from the related biography."""
        if obj.biography and obj.biography.character:
            return obj.biography.character.name
        return "No Character"
    
    character_name.short_description = "Character Name"
    character_name.admin_order_field = 'biography__character__name'
    
    def big_avatar_preview(self, obj):
        if obj.big_avatar:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.big_avatar.url)
        return "No Image"
    
    big_avatar_preview.short_description = "Big Avatar Preview"
    
    def small_avatar_preview(self, obj):
        if obj.small_avatar:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.small_avatar.url)
        return "No Image"
    
    small_avatar_preview.short_description = "Small Avatar Preview"
