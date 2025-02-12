from django.contrib import admin
from django.utils.html import format_html

from .models import Bargain, OfferedItem


@admin.register(Bargain)
class BargainAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'side_a_display',
        'side_a_accepted',
        'side_b_display',
        'side_b_accepted',
        'cancelled',
        'completed',
    )
    list_filter = ('cancelled', 'completed', 'side_a_accepted', 'side_b_accepted')
    search_fields = ('id', 'side_a__name', 'side_b__name')
    filter_horizontal = ('side_a_offered_items', 'side_b_offered_items')
    readonly_fields = ('side_a_offered_items_preview', 'side_b_offered_items_preview')

    def side_a_display(self, obj):
        if obj.side_a:
            pictogram = format_html('<span style="color: blue;">&#128309;</span> ')
            avatar = ""
            if (hasattr(obj.side_a, 'biography') and obj.side_a.biography and
                    getattr(obj.side_a.biography, 'avatar', None)):
                avatar = format_html(
                    '<img src="{}" style="height: 40px; width: 40px; border-radius: 50%; margin-right: 5px;" />',
                    obj.side_a.biography.avatar.url
                )
            return format_html('{}{}{}', pictogram, avatar, obj.side_a)
        return "No Character"
    side_a_display.short_description = "Side A"

    def side_b_display(self, obj):
        if obj.side_b:
            pictogram = format_html('<span style="color: red;">&#128308;</span> ')
            avatar = ""
            if (hasattr(obj.side_b, 'biography') and obj.side_b.biography and
                    getattr(obj.side_b.biography, 'avatar', None)):
                avatar = format_html(
                    '<img src="{}" style="height: 40px; width: 40px; border-radius: 50%; margin-right: 5px;" />',
                    obj.side_b.biography.avatar.url
                )
            return format_html('{}{}{}', pictogram, avatar, obj.side_b)
        return "No Character"
    side_b_display.short_description = "Side B"

    def side_a_offered_items_preview(self, obj):
        # Add side A's avatar to the header if available
        avatar = ""
        if obj.side_a and hasattr(obj.side_a, 'biography') and obj.side_a.biography and getattr(obj.side_a.biography, 'avatar', None):
            avatar = format_html(
                '<img src="{}" style="height: 40px; width: 40px; border-radius: 50%; margin-right: 5px;" />',
                obj.side_a.biography.avatar.url
            )
        header = format_html(
            '<div style="margin-bottom: 5px;">{}<strong style="color: blue;">&#128309; Side A Items:</strong></div>',
            avatar
        )
        items_html = ""
        for offered in obj.side_a_offered_items.all():
            if offered.item.icon:
                items_html += format_html(
                    '<img src="{}" style="height: 40px; width: 40px; margin: 2px;" />',
                    offered.item.icon.url
                )
        return format_html('{}{}', header, items_html) if items_html else "No Items"
    side_a_offered_items_preview.short_description = "Side A Offered Items"

    def side_b_offered_items_preview(self, obj):
        # Add side B's avatar to the header if available
        avatar = ""
        if obj.side_b and hasattr(obj.side_b, 'biography') and obj.side_b.biography and getattr(obj.side_b.biography, 'avatar', None):
            avatar = format_html(
                '<img src="{}" style="height: 40px; width: 40px; border-radius: 50%; margin-right: 5px;" />',
                obj.side_b.biography.avatar.url
            )
        header = format_html(
            '<div style="margin-bottom: 5px;">{}<strong style="color: red;">&#128308; Side B Items:</strong></div>',
            avatar
        )
        items_html = ""
        for offered in obj.side_b_offered_items.all():
            if offered.item.icon:
                items_html += format_html(
                    '<img src="{}" style="height: 40px; width: 40px; margin: 2px;" />',
                    offered.item.icon.url
                )
        return format_html('{}{}', header, items_html) if items_html else "No Items"
    side_b_offered_items_preview.short_description = "Side B Offered Items"


@admin.register(OfferedItem)
class OfferedItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'bargain', 'item_icon', 'item')
    search_fields = ('id', 'item__name')
    list_filter = ('bargain',)

    def item_icon(self, obj):
        if obj.item.icon:
            return format_html(
                '<img src="{}" style="height: 50px; width: 50px; border-radius: 5px;" />',
                obj.item.icon.url
            )
        return "No Icon"
    item_icon.short_description = "Item Icon"
