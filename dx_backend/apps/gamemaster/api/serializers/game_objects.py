from rest_framework import serializers

from apps.character.models import Character
from apps.core.models import GameObject, DimensionAnomaly
from apps.items.models import WorldItem


class CharacterPolymorphicSerializer(serializers.ModelSerializer):
    """Serializer for Character objects"""
    class Meta:
        model = Character
        fields = ['id', 'position', 'dimension', 'is_active', 'campaign', 'name', 'owner', 'organization', 
                 'tags', 'path', 'rank', 'experience', 'current_health_points', 'current_energy_points', 
                 'current_active_points', 'place_of_birth', 'school_slots', 'npc', 'behavior', 
                 'last_safe_position', 'resetting_base_stats']


class WorldItemPolymorphicSerializer(serializers.ModelSerializer):
    """Serializer for WorldItem objects"""
    class Meta:
        model = WorldItem
        fields = ['id', 'position', 'dimension', 'is_active', 'campaign', 'item', 'charges_left', 'visibility']


class DimensionAnomalyPolymorphicSerializer(serializers.ModelSerializer):
    """Serializer for DimensionAnomaly objects"""
    class Meta:
        model = DimensionAnomaly
        fields = ['id', 'position', 'dimension', 'is_active', 'campaign', 'known', 'level', 'effect']


class GameObjectSerializer(serializers.ModelSerializer):
    # Add a field to get the polymorphic type of the object
    object_type = serializers.SerializerMethodField()
    # Add a field to get the real instance data
    real_instance = serializers.SerializerMethodField()

    class Meta:
        model = GameObject
        fields = ['id', 'position', 'dimension', 'is_active', 'campaign', 'object_type', 'real_instance']

    def get_object_type(self, obj):
        # Get the real instance using Django Polymorphic's get_real_instance method
        real_instance = obj.get_real_instance()
        # Get the content type information
        content_type = real_instance.polymorphic_ctype
        # Return a dictionary with detailed type information
        return {
            'model': content_type.model,
            'app_label': content_type.app_label,
            'name': real_instance.__class__.__name__
        }

    def get_real_instance(self, obj):
        """
        Return the serialized data for the real instance of the GameObject.
        This allows clients to access the specific fields of the subclass.
        """
        real_instance = obj.get_real_instance()
        instance_class = real_instance.__class__

        # Choose the appropriate serializer based on the instance class
        if instance_class == Character:
            serializer = CharacterPolymorphicSerializer(real_instance)
            return serializer.data
        elif instance_class == WorldItem:
            serializer = WorldItemPolymorphicSerializer(real_instance)
            return serializer.data
        elif instance_class == DimensionAnomaly:
            serializer = DimensionAnomalyPolymorphicSerializer(real_instance)
            return serializer.data
        else:
            # For unknown types, just return the base fields
            return {
                'id': real_instance.id,
                'position': real_instance.position_id if real_instance.position else None,
                'dimension': real_instance.dimension_id if real_instance.dimension else None,
                'is_active': real_instance.is_active,
                'campaign': real_instance.campaign_id if real_instance.campaign else None,
            }
