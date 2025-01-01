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
    to_position = serializers.SerializerMethodField()

    def get_to_position(self, obj):
        if obj.position_from == self.context.get('current_position'):
            return obj.position_to.id
        return obj.position_from.id

    class Meta:
        model = PositionConnection
        fields = ('to_position', 'is_active', 'is_public', 'direction', "is_locked")

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
        # FIXME: Fix Coordinates to Direction mapping
        direction_map = {
            (-1, -1, 0): DirectionEnum.NORTHWEST,

            (0, -1, 0): DirectionEnum.NORTH,

            (1, -1, 0): DirectionEnum.NORTH_EAST,

            (1, 0, 0): DirectionEnum.EAST,

            (-1, 0, 0): DirectionEnum.WEST,

            (-1, 1, 0): DirectionEnum.SOUTH_WEST,

            (0, 1, 0): DirectionEnum.SOUTH,
            (1, 1, 0): DirectionEnum.SOUTH_EAST,

            (0, 0, 1): DirectionEnum.UP,
            (0, 0, -1): DirectionEnum.DOWN,
        }
        # direction_map = {
        #     (-1, 1, 0): DirectionEnum.NORTHWEST,
        #     (0, 1, 0): DirectionEnum.NORTH,
        #     (1, 1, 0): DirectionEnum.NORTH_EAST,
        #     (1, 0, 0): DirectionEnum.EAST,
        #     (-1, 0, 0): DirectionEnum.WEST,
        #     (-1, -1, 0): DirectionEnum.SOUTH_WEST,
        #     (0, -1, 0): DirectionEnum.SOUTH,
        #     (1, -1, 0): DirectionEnum.SOUTH_EAST,
        #
        #     (0, 0, 1): DirectionEnum.UP,
        #     (0, 0, -1): DirectionEnum.DOWN,
        # }

        return direction_map.get((dx, dy, dz), None)


class TeleportCoordinatesSerializer(serializers.Serializer):
    """References an existing position by coordinates only."""
    grid_x = serializers.IntegerField()
    grid_y = serializers.IntegerField()
    grid_z = serializers.IntegerField()

    def is_valid(self, *args, raise_exception=False):
        try:
            super().is_valid(raise_exception=raise_exception)
            try:
                self.instance = Position.objects.get(
                    grid_x=self.validated_data['grid_x'],
                    grid_y=self.validated_data['grid_y'],
                    grid_z=self.validated_data['grid_z']
                )
                return True
            except Position.DoesNotExist:
                raise serializers.ValidationError("Position does not exist.")
        except serializers.ValidationError:
            if raise_exception:
                raise
            return False

    def create(self, validated_data):
        return self.instance

    def update(self, instance, validated_data):
        return instance


class TeleportPositionSerializer(serializers.Serializer):
    """References an existing position by ID only."""
    id = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())

    # No create/update needed; we just pull an existing Position
    def create(self, validated_data):
        return validated_data['id']

    def update(self, instance, validated_data):
        return instance


class PositionSerializer(serializers.ModelSerializer):
    connections = serializers.SerializerMethodField()
    location = serializers.UUIDField(source='sub_location.location_id')
    characters = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = (
            'id', 'grid_x', 'grid_y', 'grid_z', 'sub_location', "location", 'labels', 'connections', 'characters',
            "image")

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

    def get_characters(self, obj):
        """Retrieve all characters in the current position."""
        return [character.id for character in obj.characters.all()]

    def get_image(self, obj):
        """Retrieve the background of the current position."""
        # if obj.image return obj.image.url if not take sub_location.image if not take location.image if not take area.image if not take city.image
        image = None
        if obj.image:
            image = obj.image.url
        elif obj.sub_location.image:
            image = obj.sub_location.image.url
        elif obj.sub_location.location.image:
            image = obj.sub_location.location.image.url
        elif obj.sub_location.location.area.image:
            image = obj.sub_location.location.area.image.url
        elif obj.sub_location.location.area.city.image:
            image = obj.sub_location.location.area.city.image.url
        # the image url must be extended with context from the seraializer this bihaveior is standard in the rest framework
        if image:
            request = self.context.get('request')
            return request.build_absolute_uri(image)
        return image
