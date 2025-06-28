from rest_framework import serializers

from apps.world.models import Position, PositionConnection, SubLocation
from apps.world.api.serializers.openapi import PositionRelationConfigurationSerializer


class SubLocationSerializer(serializers.ModelSerializer):
    """
    Serializer for SubLocation model.
    """

    class Meta:
        model = SubLocation
        fields = ['id', 'name', 'description', 'location', 'is_active']


class PositionSerializer(serializers.ModelSerializer):
    """
    Serializer for Position model.
    """
    sub_location_details = SubLocationSerializer(source='sub_location', read_only=True)

    class Meta:
        model = Position
        fields = ['id', 'grid_x', 'grid_y', 'grid_z', 'sub_location', 'sub_location_details', 'labels', 'is_safe',
                  'image', 'coordinates']
        read_only_fields = ['coordinates']


class PositionConnectionSerializer(serializers.ModelSerializer):
    """
    Serializer for PositionConnection model.
    """
    position_from_details = PositionSerializer(source='position_from', read_only=True)
    position_to_details = PositionSerializer(source='position_to', read_only=True)

    class Meta:
        model = PositionConnection
        fields = ['id', 'position_from', 'position_to', 'position_from_details', 'position_to_details',
                  'locked', 'is_active', 'is_public', 'is_vertical', 'is_horizontal', 'config']
        read_only_fields = ['is_vertical', 'is_horizontal']

    def to_representation(self, instance):
        """
        Override to_representation to maintain backward compatibility with 'is_locked' field.
        """
        ret = super().to_representation(instance)
        ret['is_locked'] = ret['locked']
        return ret

    def create(self, validated_data):
        """
        Override create method to handle nested config data.
        """
        config_data = validated_data.pop('config', {})
        instance = super().create(validated_data)
        if config_data:
            instance.config = config_data
            instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        Override update method to handle nested config data.
        """
        config_data = validated_data.pop('config', None)
        instance = super().update(instance, validated_data)
        if config_data is not None:
            instance.config = config_data
            instance.save()
        return instance


class GridZParameterSerializer(serializers.Serializer):
    """
    Serializer for grid_z parameter filtering.
    """
    grid_z = serializers.IntegerField(required=False, help_text="Filter by grid_z coordinate")


class PositionMoveSerializer(serializers.Serializer):
    """
    Serializer for moving a position to new coordinates.
    """
    grid_x = serializers.IntegerField(help_text="New X coordinate")
    grid_y = serializers.IntegerField(help_text="New Y coordinate")
    grid_z = serializers.IntegerField(help_text="New Z coordinate")


class PositionConnectionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a connection between two positions.
    """
    position_from = serializers.UUIDField(
        help_text="Source position UUID - identifies the starting point of the connection")
    position_to = serializers.UUIDField(
        help_text="Target position UUID - identifies the ending point of the connection")
    locked = serializers.BooleanField(help_text="Controls whether players can traverse this connection", required=False,
                                      default=False)
    is_active = serializers.BooleanField(help_text="Determines if the connection is currently usable in the game",
                                         required=False, default=True)
    is_public = serializers.BooleanField(help_text="Indicates if the connection is visible to all players",
                                         required=False, default=True)

    class Meta:
        model = PositionConnection
        fields = ['position_from', 'position_to', 'locked', 'is_active', 'is_public']


class MapResponseSerializer(serializers.Serializer):
    """
    Response serializer for the map endpoint.
    """
    positions = PositionSerializer(many=True)
    connections = PositionConnectionSerializer(many=True)
