from django.contrib import admin
from .models import Modificator, StatModificator, PlayerModificator


class StatModificatorInline(admin.TabularInline):
    model = StatModificator
    extra = 1  # Number of extra empty forms to display by default
    fields = ('stat', 'value')
    min_num = 1  # Enforce at least one StatModificator


@admin.register(Modificator)
class ModificatorAdmin(admin.ModelAdmin):
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
    inlines = [StatModificatorInline]  # Include StatModificator inline in Modificator admin

    def icon_display(self, obj):
        if obj.icon:
            return f"Icon Uploaded: {obj.icon.url.split('/')[-1]}"
        return "No Icon"
    icon_display.short_description = "Icon Status"


@admin.register(PlayerModificator)
class PlayerModificatorAdmin(admin.ModelAdmin):
    list_display = ('player', 'modificator')
    list_filter = ('player', 'modificator')
    search_fields = ('player__name', 'modificator__name')  # Assuming `Player` and `Modificator` have `name` fields
    readonly_fields = ('id', 'created_at', 'updated_at')  # Assuming BaseModel includes these fields
    fieldsets = (
        (None, {
            'fields': ('player', 'modificator')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at')
        }),
    )
    list_per_page = 20  # To manage pagination for larger datasets

@admin.register(StatModificator)
class StatModificatorAdmin(admin.ModelAdmin):
    list_display = ('modificator', 'stat', 'value')
    list_filter = ('modificator', 'stat')
    search_fields = ('modificator__name', 'stat__name')  # Assuming `PlayerStat` has a `name` field
    readonly_fields = ('id', 'created_at', 'updated_at')  # Assuming BaseModel includes these fields
    fieldsets = (
        (None, {
            'fields': ('modificator', 'stat', 'value')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at')
        }),
    )
    list_per_page = 20  # To manage pagination for larger datasets