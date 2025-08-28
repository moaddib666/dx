from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from polymorphic.admin import PolymorphicChildModelAdmin

from apps.core.admin.mixins import CampaignAdminMixin
from apps.spawner.models import NPCSpawner
from .spawner import SpawnedEntityInline


@admin.register(NPCSpawner)
class NPCSpawnerAdmin(CampaignAdminMixin, PolymorphicChildModelAdmin):
    """
    Admin interface for managing NPC spawners.
    Specialized admin for spawning NPCs from character templates.
    """
    base_model = NPCSpawner
    show_in_index = True
    
    list_display = [
        'id', 'character_template_link', 'position_link', 'dimension_link',
        'is_active', 'spawn_limit', 'spawned_count', 'next_spawn_cycle_number'
    ]
    list_filter = [
        'is_active',
        'character_template',
        'dimension',
        'spawn_limit',
        'respawn_cycles'
    ]
    search_fields = [
        'id', 
        'character_template__name',
        'character_template__biography_template__name',
        'position__name', 
        'dimension__name'
    ]
    readonly_fields = ['spawned_count', 'campaign_link', 'next_spawn_cycle_number']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('campaign_link', 'is_active')
        }),
        ('NPC Configuration', {
            'fields': ('character_template',),
            'description': 'Select the character template to spawn NPCs from'
        }),
        ('Location', {
            'fields': ('position', 'dimension'),
            'description': 'Set the spawner location in the game world'
        }),
        ('Spawn Configuration', {
            'fields': ('spawn_limit', 'respawn_cycles', 'next_spawn_cycle_number'),
            'description': 'Configure how many NPCs to spawn and respawn timing'
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
        'clear_spawned_entities',
        'spawn_npcs_now'
    ]
    
    def get_queryset(self, request):
        """Optimize queryset with related objects."""
        return super().get_queryset(request).select_related(
            'character_template',
            'character_template__biography_template',
            'position', 
            'dimension', 
            'campaign'
        ).prefetch_related('spawned_entities')
    
    def character_template_link(self, obj):
        """Create a link to the character template admin."""
        if obj.character_template:
            url = reverse('admin:character_charactertemplate_change', args=[obj.character_template.pk])
            template_name = obj.character_template.biography_template.name if obj.character_template.biography_template else str(obj.character_template)
            return format_html('<a href="{}">{}</a>', url, template_name)
        return '-'
    character_template_link.short_description = 'Character Template'
    character_template_link.admin_order_field = 'character_template__biography_template__name'
    
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
        """Display the number of currently spawned NPCs."""
        return obj.spawned_entities.count()
    spawned_count.short_description = 'Spawned NPCs'
    
    def activate_spawners(self, request, queryset):
        """Activate selected NPC spawners."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} NPC spawner(s) activated.')
    activate_spawners.short_description = 'Activate selected NPC spawners'
    
    def deactivate_spawners(self, request, queryset):
        """Deactivate selected NPC spawners."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} NPC spawner(s) deactivated.')
    deactivate_spawners.short_description = 'Deactivate selected NPC spawners'
    
    def reset_spawn_cycles(self, request, queryset):
        """Reset spawn cycles for selected NPC spawners."""
        updated = queryset.update(next_spawn_cycle_number=0)
        self.message_user(request, f'Spawn cycles reset for {updated} NPC spawner(s).')
    reset_spawn_cycles.short_description = 'Reset spawn cycles'
    
    def clear_spawned_entities(self, request, queryset):
        """Clear all spawned NPCs for selected spawners."""
        total_cleared = 0
        for spawner in queryset:
            count = spawner.spawned_entities.count()
            spawner.spawned_entities.all().delete()
            total_cleared += count
        self.message_user(request, f'Cleared {total_cleared} spawned NPCs.')
    clear_spawned_entities.short_description = 'Clear spawned NPCs'
    
    def spawn_npcs_now(self, request, queryset):
        """Manually trigger NPC spawning for selected spawners."""
        spawned_count = 0
        for spawner in queryset.filter(is_active=True):
            # This would integrate with the actual spawning service
            # For now, we'll just show a message
            spawned_count += 1
        
        if spawned_count > 0:
            self.message_user(request, f'Triggered spawning for {spawned_count} active NPC spawner(s).')
        else:
            self.message_user(request, 'No active spawners selected for manual spawning.', level='warning')
    spawn_npcs_now.short_description = 'Spawn NPCs now (manual trigger)'