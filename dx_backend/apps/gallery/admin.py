from django.contrib import admin
from django.utils.html import format_html

from .models import Art


@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    list_display = ('name', 'canonical', 'preview')  # Include preview in the list display
    list_filter = ('canonical',)
    search_fields = ('name', 'description')
    actions = ['make_canonical']

    def preview(self, obj):
        """
        Generate an HTML preview of the image.
        """
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "No Image"

    preview.short_description = "Image Preview"

    def make_canonical(self, request, queryset):
        """
        Custom admin action to set canonical to True for selected items.
        """
        updated = queryset.update(canonical=True)
        self.message_user(request, f"{updated} item(s) were marked as canonical.")

    make_canonical.short_description = "Mark selected items as canonical"
