from django.contrib import admin
from .models import CurrencyToken, PlayerCurrency


@admin.register(CurrencyToken)
class CurrencyTokenAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon_display')
    search_fields = ('name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')  # Assuming BaseModel includes these fields
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'icon')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at')
        }),
    )

    def icon_display(self, obj):
        if obj.icon:
            return f"Icon Uploaded: {obj.icon.url.split('/')[-1]}"
        return "No Icon"
    icon_display.short_description = "Icon Status"


@admin.register(PlayerCurrency)
class PlayerCurrencyAdmin(admin.ModelAdmin):
    list_display = ('player', 'currency', 'amount')
    list_filter = ('player', 'currency')
    search_fields = ('player__name', 'currency__name')  # Assuming Player and CurrencyToken have `name` fields
    readonly_fields = ('id', 'created_at', 'updated_at')  # Assuming BaseModel includes these fields
    fieldsets = (
        (None, {
            'fields': ('player', 'currency', 'amount')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at')
        }),
    )
    list_per_page = 20  # To control pagination for large datasets
