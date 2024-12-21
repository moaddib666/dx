from django.contrib import admin
from .models import Item, PlayerItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'type', 'weight', 'ap_cost', 'hp_cost', 'ep_cost',
        'once_per_fight', 'once_per_turn', 'once', 'canonical'
    )
    list_filter = ('type', 'once_per_fight', 'once_per_turn', 'once', 'canonical')
    search_fields = ('name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')  # Assuming BaseModel includes these fields
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'icon', 'type', 'weight', 'canonical')
        }),
        ('Costs', {
            'fields': ('ap_cost', 'hp_cost', 'ep_cost')
        }),
        ('Usage Restrictions', {
            'fields': ('once_per_fight', 'once_per_turn', 'once')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at')
        }),
    )
    list_per_page = 20  # To control pagination for large datasets


@admin.register(PlayerItem)
class PlayerItemAdmin(admin.ModelAdmin):
    list_display = ('player', 'item', 'amount')
    list_filter = ('player', 'item__type')  # Filters by player and item type
    search_fields = ('player__name', 'item__name')  # Assuming Player and Item have `name` fields
    readonly_fields = ('id', 'created_at', 'updated_at')  # Assuming BaseModel includes these fields
    fieldsets = (
        (None, {
            'fields': ('player', 'item', 'amount')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at')
        }),
    )
    list_per_page = 20  # To control pagination for large datasets
