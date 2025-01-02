from django.utils.html import format_html
from django.urls import re_path
import uuid
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from polymorphic.admin import PolymorphicChildModelAdmin

from .models import Item, CharacterItem, WorldItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'type', 'weight', 'canonical', 'icon_preview'
    )
    list_filter = ('type', 'canonical')
    search_fields = ('name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at', 'icon_preview')  # Adding icon_preview as readonly
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'icon', 'icon_preview', 'type', 'weight', 'canonical')
        }),
        ('Advanced', {
            'fields': ('skill', 'effect')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at')
        }),
    )
    list_per_page = 20  # To control pagination for large datasets

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                f'<img src="{obj.icon.url}" style="height: 50px; width: 50px; border-radius: 5px;" alt="Item Icon" />'
            )
        return "No Icon Available"

    icon_preview.short_description = "Icon Preview"


@admin.register(WorldItem)
class WorldItemAdmin(PolymorphicChildModelAdmin):
    base_model = WorldItem
    show_in_index = True
    list_display = ('item', 'position', 'icon_preview')
    list_filter = ('item__type',)
    search_fields = ('id', 'item__name', 'position')

    def icon_preview(self, obj):
        if obj.item.icon:
            return format_html(
                f'<img src="{obj.item.icon.url}" style="height: 50px; width: 50px; border-radius: 5px;" alt="Item Icon" />'
            )
        return "No Icon Available"

    icon_preview.short_description = "Icon Preview"


@admin.register(CharacterItem)
class CharacterItemAdmin(admin.ModelAdmin):
    list_display = ('character', 'get_world_item_name', 'icon_preview')
    list_filter = ('character', 'world_item__item__type')  # Filters by character and item type
    search_fields = ('character__name', 'world_item__item__name')  # Assuming Character and Item have `name` fields
    readonly_fields = ('id', 'created_at', 'updated_at', 'icon_preview')  # Adding icon_preview as readonly
    fieldsets = (
        (None, {
            'fields': ('character', 'world_item', 'icon_preview')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at')
        }),
    )
    list_per_page = 20  # To control pagination for large datasets

    def get_world_item_name(self, obj):
        return obj.world_item.item.name

    get_world_item_name.short_description = 'Item Name'

    def icon_preview(self, obj):
        if obj.world_item and obj.world_item.item.icon:
            return format_html(
                f'<img src="{obj.world_item.item.icon.url}" style="height: 50px; width: 50px; border-radius: 5px;" alt="Item Icon" />'
            )
        return "No Icon Available"

    icon_preview.short_description = "Icon Preview"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r'^(?P<item_id>[a-f0-9\-]+)/duplicate/$',
                self.admin_site.admin_view(self.duplicate_item),
                name='duplicate_item',
            ),
        ]
        return custom_urls + urls

    def duplicate_item(self, request, item_id):
        # Ensure the item_id is valid UUID
        try:
            uuid.UUID(item_id)
        except ValueError:
            self.message_user(request, "Invalid UUID", level="error")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        item = get_object_or_404(CharacterItem, pk=item_id)
        item.pk = None  # Reset the primary key to create a new object
        item.save()
        self.message_user(request, "Item duplicated successfully.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
