from rest_framework import serializers

from apps.spawner.models import NPCSpawner, SpawnedEntity


class SpawnedEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpawnedEntity
        fields = [
            'id',
            'game_object',
        ]
        read_only_fields = fields


class NPCGenericSpawnerSerializer(serializers.ModelSerializer):
    """
    Serializer for NPCSpawner model for Game Master API.
    
    This serializer provides complete functionality for creating and managing
    NPC spawners with position, campaign, character template, and spawn settings.
    """

    spawned_entities = SpawnedEntitySerializer(many=True, read_only=True)

    class Meta:
        model = NPCSpawner
        fields = [
            'id',
            'is_active',
            'spawn_limit',
            'respawn_cycles',
            'character_template',
            'next_spawn_cycle_number',
            'dimension',
            'position',
            'campaign',
            'spawned_entities',
        ]
        read_only_fields = [
            "id",
            "next_spawn_cycle_number",
            "spawned_entities",
        ]


class NPCSpawnerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPCSpawner
        fields = [
            'spawn_limit',
            'respawn_cycles',
            'character_template',
            'dimension',
            'position',
            'campaign',
            'is_active',
            'id',
        ]
        read_only_fields = [
            "id",
            "is_active",
        ]


class NPCSpawnerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPCSpawner
        fields = [
            'id',
            'is_active',
            'spawn_limit',
            'respawn_cycles',
            'character_template',
            'next_spawn_cycle_number',
            'dimension',
            'position',
            'campaign',
        ]
        read_only_fields = fields
