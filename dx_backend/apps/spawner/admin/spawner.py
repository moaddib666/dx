from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelFilter

from apps.core.admin import CampaignModelAdmin
from apps.spawner.models import Spawner, SpawnedEntity


class SpawnedEntityInline(admin.TabularInline):
    """Inline for managing spawned entities within a spawner."""
    model = SpawnedEntity
    extra = 0
    readonly_fields = ('spawned_at', 'game_object_link')
    fields = ('game_object_link', 'spawned_at')
    
    def game_object_link(self, obj):
        """Create a link to the spawned game object."""
        if obj.game_object:
            url = reverse('admin:core_gameobject_change', args=[obj.game_object.pk])
            return format_html('<a href="{}">{}</a>', url, obj.game_object)
        return '-'
    game_object_link.short_description = 'Game Object'


@admin.register(Spawner)
class SpawnerAdmin(CampaignModelAdmin, PolymorphicParentModelAdmin):
    """
    Admin interface for managing spawners.
    Provides game masters with comprehensive spawner management capabilities.
    """
    base_model = Spawner
    child_models = []  # Will be populated by child admin classes
    
    list_display = [
        'id', 'polymorphic_ctype', 'position_link', 'dimension_link', 
        'is_active', 'spawn_limit', 'spawned_count', 'next_spawn_cycle_number'
    ]
    list_filter = [
        PolymorphicChildModelFilter,
        'is_active',
        'dimension',
        'spawn_limit',
        'respawn_cycles'
    ]
    search_fields = ['id', 'position__name', 'dimension__name']
    readonly_fields = ['spawned_count', 'campaign_link']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('campaign_link', 'is_active')
        }),
        ('Location', {
            'fields': ('position', 'dimension'),
            'description': 'Set the spawner location in the game world'
        }),
        ('Spawn Configuration', {
            'fields': ('spawn_limit', 'respawn_cycles', 'next_spawn_cycle_number'),
            'description': 'Configure how many entities to spawn and respawn timing'
        }),
        ('Statistics', {
            'fields': ('spawned_count',),
            'classes': ('collapse',)
        })
    )
    
    inlines = [SpawnedEntityInline]
    
    actions = [
        'activate_spawners',
        'deactivate_spawners',
        'reset_spawn_cycles',
        'clear_spawned_entities'
    ]
    
    def get_queryset(self, request):
        """Optimize queryset with related objects."""
        return super().get_queryset(request).select_related(
            'position', 'dimension', 'campaign'
        ).prefetch_related('spawned_entities')
    
    def position_link(self, obj):
        """Create a link to the position admin."""
        if obj.position:
            url = reverse('admin:world_position_change', args=[obj.position.pk])
            return format_html('<a href="{}">{}</a>', url, obj.position)
        return '-'
    position_link.short_description = 'Position'
    position_link.admin_order_field = 'position__name'
    
    def dimension_link(self, obj):
        """Create a link to the dimension admin."""
        if obj.dimension:
            url = reverse('admin:world_dimension_change', args=[obj.dimension.pk])
            return format_html('<a href="{}">{}</a>', url, obj.dimension)
        return '-'
    dimension_link.short_description = 'Dimension'
    dimension_link.admin_order_field = 'dimension__name'
    
    def campaign_link(self, obj):
        """Create a link to the campaign admin."""
        if obj.campaign:
            url = reverse('admin:game_campaign_change', args=[obj.campaign.pk])
            return format_html('<a href="{}">{}</a>', url, obj.campaign)
        return '-'
    campaign_link.short_description = 'Campaign'
    
    def spawned_count(self, obj):
        """Display the number of currently spawned entities."""
        return obj.spawned_entities.count()
    spawned_count.short_description = 'Spawned Entities'
    
    def activate_spawners(self, request, queryset):
        """Activate selected spawners."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} spawner(s) activated.')
    activate_spawners.short_description = 'Activate selected spawners'
    
    def deactivate_spawners(self, request, queryset):
        """Deactivate selected spawners."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} spawner(s) deactivated.')
    deactivate_spawners.short_description = 'Deactivate selected spawners'
    
    def reset_spawn_cycles(self, request, queryset):
        """Reset spawn cycles for selected spawners."""
        updated = queryset.update(next_spawn_cycle_number=0)
        self.message_user(request, f'Spawn cycles reset for {updated} spawner(s).')
    reset_spawn_cycles.short_description = 'Reset spawn cycles'
    
    def clear_spawned_entities(self, request, queryset):
        """Clear all spawned entities for selected spawners."""
        total_cleared = 0
        for spawner in queryset:
            count = spawner.spawned_entities.count()
            spawner.spawned_entities.all().delete()
            total_cleared += count
        self.message_user(request, f'Cleared {total_cleared} spawned entities.')
    clear_spawned_entities.short_description = 'Clear spawned entities'