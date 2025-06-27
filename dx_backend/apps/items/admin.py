from django.utils.html import format_html
from django.urls import re_path
import uuid
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from polymorphic.admin import PolymorphicChildModelAdmin
from apps.core.admin.mixins import CampaignAdminMixin
from apps.core.admin import CampaignModelAdmin

from .models import Item, CharacterItem, WorldItem


class NPCFilter(SimpleListFilter):
    title = _('Character Type')
    parameter_name = 'character__npc'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Yes')),
            ('0', _('No')),
            ('all', _('All')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(character__npc=True)
        elif self.value() == '0':
            return queryset.filter(character__npc=False)
        return queryset

    def choices(self, changelist):
        # Default to showing only non-NPCs
        all_choice = next(super().choices(changelist))
        all_choice['selected'] = self.value() is None
        yield all_choice

        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'type', 'weight', 'canonical', 'icon_preview', "skill",
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
class WorldItemAdmin(CampaignAdminMixin, PolymorphicChildModelAdmin):
    base_model = WorldItem
    show_in_index = True
    list_display = ('item', 'position', 'icon_preview', 'campaign')
    list_filter = ('item__type', 'campaign')
    search_fields = ('id', 'item__name', 'position')

    def icon_preview(self, obj):
        if obj.item.icon:
            return format_html(
                f'<img src="{obj.item.icon.url}" style="height: 50px; width: 50px; border-radius: 5px;" alt="Item Icon" />'
            )
        return "No Icon Available"

    icon_preview.short_description = "Icon Preview"


@admin.register(CharacterItem)
class CharacterItemAdmin(CampaignModelAdmin):
    list_display = ('character', 'get_world_item_name', 'icon_preview')
    list_filter = (NPCFilter, 'character__organization', 'character',
                   'world_item__item__type')  # Added NPC and organization filters
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        campaign_id = request.session.get('campaign_id')

        # Filter by campaign
        if campaign_id:
            qs = qs.filter(world_item__campaign_id=campaign_id)

        # By default, show only non-NPC characters unless explicitly filtered
        if not request.GET.get('character__npc'):
            qs = qs.filter(character__npc=False)

        return qs

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
