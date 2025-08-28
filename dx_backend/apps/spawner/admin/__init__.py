# Spawner Admin Module
# This file imports all admin classes for the spawner app
# Each admin class is defined in separate files for better organization

from .spawner import SpawnerAdmin, SpawnedEntityInline
from .npc_spawner import NPCSpawnerAdmin
from .spawned_entity import SpawnedEntityAdmin

# All admin classes are automatically registered via @admin.register decorators
# in their respective files:
# - SpawnerAdmin: Base polymorphic parent admin for all spawner types
# - NPCSpawnerAdmin: Specialized admin for NPC spawners with character template management
# - SpawnedEntityAdmin: Admin for tracking and managing spawned entities