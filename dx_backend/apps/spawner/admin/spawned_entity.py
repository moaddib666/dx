from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from apps.core.admin import CampaignModelAdmin
from apps.spawner.models import SpawnedEntity


@admin.register(SpawnedEntity)
class SpawnedEntityAdmin(CampaignModelAdmin):
    """
    Admin interface for managing spawned entities.
    Provides game masters with tracking and management of all spawned entities.
    """
    
    list_display = [
        'id', 'spawner_link', 'game_object_link', 'spawned_at_link', 
        'spawner_type', 'spawner_active', 'created_at'
    ]
    list_filter = [
        'spawner__polymorphic_ctype',
        'spawner__is_active',
        'spawned_at',
        'created_at'
    ]
    search_fields = [
        'id',
        'spawner__id',
        'game_object__id',
        'spawner__position__name',
        'spawner__dimension__name'
    ]
    readonly_fields = [
        'spawner_link', 'game_object_link', 'spawned_at_link',
        'spawner_type', 'spawner_position', 'spawner_dimension',
        'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Entity Information', {
            'fields': ('spawner_link', 'game_object_link', 'spawned_at_link')
        }),
        ('Spawner Details', {
            'fields': ('spawner_type', 'spawner_position', 'spawner_dimension'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = [
        'remove_entities',
        'respawn_entities',
        'move_to_spawner_position'
    ]
    
    def get_queryset(self, request):
        """Optimize queryset with related objects."""
        return super().get_queryset(request).select_related(
            'spawner',
            'spawner__position',
            'spawner__dimension',
            'spawner__campaign',
            'game_object',
            'spawned_at'
        )
    
    def spawner_link(self, obj):
        """Create a link to the spawner admin."""
        if obj.spawner:
            # Determine the correct admin URL based on spawner type
            spawner_type = obj.spawner.polymorphic_ctype.model
            if spawner_type == 'npcspawner':
                url = reverse('admin:spawner_npcspawner_change', args=[obj.spawner.pk])
            else:
                url = reverse('admin:spawner_spawner_change', args=[obj.spawner.pk])
            return format_html('<a href="{}">{} ({})</a>', url, obj.spawner.id, spawner_type.upper())
        return '-'
    spawner_link.short_description = 'Spawner'
    spawner_link.admin_order_field = 'spawner__id'
    
    def game_object_link(self, obj):
        """Create a link to the game object admin."""
        if obj.game_object:
            url = reverse('admin:core_gameobject_change', args=[obj.game_object.pk])
            return format_html('<a href="{}">{}</a>', url, obj.game_object)
        return '-'
    game_object_link.short_description = 'Game Object'
    game_object_link.admin_order_field = 'game_object__id'
    
    def spawned_at_link(self, obj):
        """Create a link to the cycle admin."""
        if obj.spawned_at:
            url = reverse('admin:action_cycle_change', args=[obj.spawned_at.pk])
            return format_html('<a href="{}">{}</a>', url, obj.spawned_at)
        return '-'
    spawned_at_link.short_description = 'Spawned At Cycle'
    spawned_at_link.admin_order_field = 'spawned_at__id'
    
    def spawner_type(self, obj):
        """Display the spawner type."""
        if obj.spawner:
            return obj.spawner.polymorphic_ctype.model.upper()
        return '-'
    spawner_type.short_description = 'Spawner Type'
    spawner_type.admin_order_field = 'spawner__polymorphic_ctype__model'
    
    def spawner_active(self, obj):
        """Display if the spawner is active."""
        if obj.spawner:
            return obj.spawner.is_active
        return False
    spawner_active.short_description = 'Spawner Active'
    spawner_active.boolean = True
    spawner_active.admin_order_field = 'spawner__is_active'
    
    def spawner_position(self, obj):
        """Display the spawner position."""
        if obj.spawner and obj.spawner.position:
            url = reverse('admin:world_position_change', args=[obj.spawner.position.pk])
            return format_html('<a href="{}">{}</a>', url, obj.spawner.position)
        return '-'
    spawner_position.short_description = 'Spawner Position'
    
    def spawner_dimension(self, obj):
        """Display the spawner dimension."""
        if obj.spawner and obj.spawner.dimension:
            url = reverse('admin:world_dimension_change', args=[obj.spawner.dimension.pk])
            return format_html('<a href="{}">{}</a>', url, obj.spawner.dimension)
        return '-'
    spawner_dimension.short_description = 'Spawner Dimension'
    
    def remove_entities(self, request, queryset):
        """Remove selected spawned entities."""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} spawned entity(ies) removed.')
    remove_entities.short_description = 'Remove selected entities'
    
    def respawn_entities(self, request, queryset):
        """Mark entities for respawning (remove and reset spawner cycle)."""
        spawners_to_reset = set()
        count = 0
        
        for entity in queryset:
            if entity.spawner:
                spawners_to_reset.add(entity.spawner)
            count += 1
        
        # Remove the entities
        queryset.delete()
        
        # Reset spawn cycles for affected spawners
        for spawner in spawners_to_reset:
            spawner.next_spawn_cycle = None
            spawner.save(update_fields=['next_spawn_cycle'])
        
        self.message_user(request, f'{count} entity(ies) removed and {len(spawners_to_reset)} spawner(s) reset for respawning.')
    respawn_entities.short_description = 'Remove and mark for respawning'
    
    def move_to_spawner_position(self, request, queryset):
        """Move game objects to their spawner positions (if applicable)."""
        moved_count = 0
        for entity in queryset:
            if (entity.game_object and entity.spawner and 
                entity.spawner.position and hasattr(entity.game_object, 'position')):
                entity.game_object.position = entity.spawner.position
                entity.game_object.save(update_fields=['position'])
                moved_count += 1
        
        if moved_count > 0:
            self.message_user(request, f'{moved_count} entity(ies) moved to spawner positions.')
        else:
            self.message_user(request, 'No entities could be moved (missing positions or incompatible objects).', level='warning')
    move_to_spawner_position.short_description = 'Move entities to spawner positions'