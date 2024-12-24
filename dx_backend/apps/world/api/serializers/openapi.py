from django.db import models
from rest_framework import serializers

from apps.character.models import Character
from apps.world.models import Area, Location, Dimension, City, SubLocation


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class SubLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubLocation
        fields = "__all__"


class AreaSerializer(serializers.ModelSerializer):
    sub_locations = SubLocationSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class DimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = "__all__"


class CharacterInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["id", "name"]


# class PositionSerializer(serializers.Serializer):
#     location = LocationSerializer(source='current_location')
#     area = AreaSerializer(source='current_location.area')
#     city = CitySerializer(source='current_location.area.city')
#     dimension = DimensionSerializer()
#     visitors = CharacterInfoSerializer(many=True, source='current_location.characters')
#
#     class Meta:
#         model = Character
#         fields = ['location', 'area', 'city', 'dimension', 'visitors']
#
# from rest_framework import serializers
# from apps.world.models import Position, PositionConnection

from rest_framework import serializers
from apps.world.models import Position, PositionConnection
from apps.core.models import DirectionEnum


class PositionConnectionSerializer(serializers.ModelSerializer):
    direction = serializers.SerializerMethodField()

    class Meta:
        model = PositionConnection
        fields = ('position_from', 'position_to', 'is_active', 'is_public', 'direction')

    def get_direction(self, obj):
        """Compute the direction based on the current position's role."""
        current_position = self.context.get('current_position')  # Pass current position via context

        if current_position is None:
            return None

        if obj.position_from == current_position:
            target = obj.position_to
        elif obj.position_to == current_position:
            target = obj.position_from
        else:
            return None  # Invalid connection for this position

        dx = target.grid_x - current_position.grid_x
        dy = target.grid_y - current_position.grid_y
        dz = target.grid_z - current_position.grid_z

        # Map grid differences to directions using DirectionEnum
        direction_map = {
            (-1, 1, 0): DirectionEnum.NORTHWEST,
            (0, 1, 0): DirectionEnum.NORTH,
            (1, 1, 0): DirectionEnum.NORTH_EAST,
            (1, 0, 0): DirectionEnum.EAST,
            (-1, 0, 0): DirectionEnum.WEST,
            (-1, -1, 0): DirectionEnum.SOUTH_WEST,
            (0, -1, 0): DirectionEnum.SOUTH,
            (1, -1, 0): DirectionEnum.SOUTH_EAST,
            (0, 0, 1): DirectionEnum.UP,
            (0, 0, -1): DirectionEnum.DOWN,
        }

        return direction_map.get((dx, dy, dz), None)


class PositionSerializer(serializers.ModelSerializer):
    connections = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = ('id', 'grid_x', 'grid_y', 'grid_z', 'sub_location', 'labels', 'connections')

    def get_connections(self, obj):
        """Retrieve all connections where the current position is involved."""
        connections = PositionConnection.objects.filter(
            models.Q(position_from=obj) | models.Q(position_to=obj)
        ).select_related('position_from', 'position_to')

        serializer = PositionConnectionSerializer(
            connections,
            many=True,
            context={'current_position': obj}  # Pass the current position to the connection serializer
        )
        return serializer.data
