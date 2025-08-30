from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.spawner.models import NPCSpawner, SpawnedEntity, Spawner


class AbstractSpawnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spawner
        fields = [
            'id',
            'position',
            'dimension',
            'is_active',
            'campaign',
        ]
        read_only_fields = fields


class GameObjectTypeSerializer(serializers.Serializer):
    model = serializers.CharField()
    app_label = serializers.CharField()
    name = serializers.CharField()


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


class GenericSpawnerSerializer(serializers.ModelSerializer):
    # Add a field to get the polymorphic type of the object
    object_type = serializers.SerializerMethodField()
    # Add a field to get the real instance data
    real_instance = serializers.SerializerMethodField()

    class Meta:
        model = Spawner
        fields = ['id', 'position', 'dimension', 'is_active', 'campaign', 'object_type', 'real_instance']

    @extend_schema_field(GameObjectTypeSerializer)
    def get_object_type(self, obj):
        # Get the real instance using Django Polymorphic's get_real_instance method
        real_instance = obj.get_real_instance()
        # Get the content type information
        content_type = real_instance.polymorphic_ctype
        # Return a dictionary with detailed type information
        return GameObjectTypeSerializer({
            'model': str(content_type.model),
            'app_label': str(content_type.app_label),
            'name': str(real_instance.__class__.__name__),
        }).data

    # Union AnyOf[NPCGenericSpawnerSerializer, AbstractSpawnerSerializer]
    @extend_schema_field({
        'oneOf': [
            NPCGenericSpawnerSerializer,
            AbstractSpawnerSerializer
        ],
        'description': 'The serialized data for the real instance of the polymorphic GameObject'
    })
    def get_real_instance(self, obj):
        """
        Return the serialized data for the real instance of the GameObject.
        This allows clients to access the specific fields of the subclass.
        """
        real_instance = obj.get_real_instance()
        instance_class = real_instance.__class__
        if instance_class == NPCSpawner:
            serializer = NPCGenericSpawnerSerializer(real_instance)
        else:
            serializer = AbstractSpawnerSerializer(real_instance)
        return serializer.data
