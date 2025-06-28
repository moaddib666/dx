from rest_framework import serializers

from apps.world.models import Position, PositionConnection
from apps.world.api.serializers.openapi import PositionRelationConfigurationSerializer


class PositionSerializer(serializers.ModelSerializer):
    """
    Serializer for Position model.
    """
    class Meta:
        model = Position
        fields = ['id', 'grid_x', 'grid_y', 'grid_z', 'sub_location', 'labels', 'is_safe', 'image', 'coordinates']
        read_only_fields = ['coordinates']


class PositionConnectionSerializer(serializers.ModelSerializer):
    """
    Serializer for PositionConnection model.
    """
    is_locked = serializers.BooleanField(source='locked', read_only=True)
    config = PositionRelationConfigurationSerializer()

    class Meta:
        model = PositionConnection
        fields = ['id', 'position_from', 'position_to', 'is_locked', 'is_active', 'is_public', 'is_vertical',
                  'is_horizontal', 'config']
