from django.db import models
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from apps.character.models import Character
from apps.game.services.character.core import CharacterService
from apps.game.services.world.position_connection import PositionConnectionService
from apps.world.models import Area, Location, Dimension, City, SubLocation, MapPosition, Map


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
from apps.core.models import DirectionEnum, DimensionAnomaly, PositionConnectionConfig, PositionConnectionRequirement


class PositionConnectionRequirementSerializer(serializers.Serializer):
    """
    Serializer for PositionConnectionRequirement objects.
    """
    item_id = serializers.UUIDField(required=False, allow_null=True)
    skill_id = serializers.UUIDField(required=False, allow_null=True)
    character_id = serializers.UUIDField(required=False, allow_null=True)


class PositionRelationConfigurationSerializer(serializers.Serializer):
    """
    Serializer for PositionConnectionConfig objects.
    """
    requirements = PositionConnectionRequirementSerializer(many=True, required=False, default=list)


class PositionConnectionSerializer(serializers.ModelSerializer):
    direction = serializers.SerializerMethodField()
    to_position = serializers.SerializerMethodField()
    is_locked = serializers.SerializerMethodField(method_name="_is_locked")
    config = PositionRelationConfigurationSerializer()

    @extend_schema_field(serializers.UUIDField())
    def get_to_position(self, obj):
        if obj.position_from == self.context.get('current_position'):
            return obj.position_to.id
        return obj.position_from.id

    class Meta:
        model = PositionConnection
        fields = ('to_position', 'is_active', 'is_public', 'direction', "is_locked", "config")

    @extend_schema_field(serializers.BooleanField())
    def _is_locked(self, obj):
        character_svc = CharacterService(self.context.get('client').main_character)
        pos_conn_svc = PositionConnectionService(obj)
        return not pos_conn_svc.is_accessible(character_svc)

    @extend_schema_field(serializers.ChoiceField(choices=DirectionEnum.choices()))
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


class WorldPositionSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = self.context.get('request').user if 'request' in self.context else None
        if not self._client:
            raise serializers.ValidationError("User context is required for PositionSerializer.")

    connections = serializers.SerializerMethodField()
    location = serializers.UUIDField(source='sub_location.location_id')
    characters = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    anomalies = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = (
            'id', 'grid_x', 'grid_y', 'grid_z', 'sub_location', "location", 'labels', 'connections', 'characters',
            "image", 'is_safe', 'anomalies')

    @extend_schema_field(serializers.ListField(child=serializers.UUIDField()))
    def get_anomalies(self, obj):
        """Retrieve all anomalies in the current position."""
        return [
            t.id for t in
            obj.gameobject_set.instance_of(DimensionAnomaly).filter(
                campaign=self._client.current_campaign
            ) if not t.known
        ]

    @extend_schema_field(serializers.ListField(child=PositionConnectionSerializer(many=True)))
    def get_connections(self, obj):
        """Retrieve all connections where the current position is involved."""
        connections = PositionConnection.objects.filter(
            models.Q(position_from=obj) | models.Q(position_to=obj)
        ).select_related('position_from', 'position_to')

        serializer = PositionConnectionSerializer(
            connections,
            many=True,
            context={'current_position': obj, "client": self._client, **self.context}
        )
        return serializer.data

    @extend_schema_field(serializers.ListField(child=serializers.UUIDField()))
    def get_characters(self, obj):
        """Retrieve all characters in the current position."""
        return [character.id for character in
                obj.gameobject_set.instance_of(Character).filter(campaign=self._client.current_campaign,
                                                                 is_active=True)]

    @extend_schema_field(serializers.CharField(allow_null=True))
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


class GenericPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'grid_x', 'grid_y', 'grid_z', 'sub_location')


class GenericPositionIdSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)

    def validate(self, attrs):
        position_id = attrs.get('id')
        if not position_id:
            raise serializers.ValidationError({"id": "This field is required."})
        try:
            # Validate that the Position exists
            self.instance = Position.objects.get(id=position_id)
        except Position.DoesNotExist:
            raise serializers.ValidationError({"id": "Position does not exist."})
        return attrs


class MapPositionSerializer(serializers.ModelSerializer):
    position = GenericPositionSerializer()

    class Meta:
        model = MapPosition
        fields = ('position', "is_active", "labels")


class MapPositionMutableSerializer(serializers.Serializer):
    position_id = serializers.UUIDField()
    labels = serializers.ListField(child=serializers.CharField(), required=False)


class NewCoordinatesSerializer(serializers.Serializer):
    grid_x = serializers.IntegerField()
    grid_y = serializers.IntegerField()
    grid_z = serializers.IntegerField()
    labels = serializers.ListField(child=serializers.CharField(), required=False)

    def validate(self, attrs):
        """ Find existing position by coordinates"""
        try:
            self.instance = Position.objects.get(
                grid_x=attrs['grid_x'],
                grid_y=attrs['grid_y'],
                grid_z=attrs['grid_z']
            )
        except Position.DoesNotExist:
            raise serializers.ValidationError("Position does not exist.")
        return attrs


class CharacterPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('id', 'position',)


class PositionConnectionMinimalSerializer(serializers.ModelSerializer):
    is_locked = serializers.BooleanField(source='locked', read_only=True)

    class Meta:
        model = PositionConnection
        fields = ('position_from', 'position_to', 'is_vertical', 'is_locked')
        read_only_fields = ('is_vertical', 'is_locked')


class MapSerializer(serializers.ModelSerializer):
    positions = serializers.SerializerMethodField()
    connections = serializers.SerializerMethodField()
    characters = serializers.SerializerMethodField()
    current_position = serializers.SerializerMethodField(
        help_text="The position of the current user's character on the map."
    )

    class Meta:
        model = Map
        fields = (
            'id', 'name', 'organization', 'is_active', 'positions', 'connections', 'characters', 'current_position')

    def _get_current_character(self):
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("Request context is required.")
        if not request.user.main_character:
            raise serializers.ValidationError("Main character is required.")
        return request.user.main_character

    def get_current_position(self, obj):
        current_character = self._get_current_character()
        return current_character.position_id

    def _get_positions(self, obj):
        return obj.map_positions.all()

    def get_positions(self, obj):
        # Fetch positions related to the map
        positions = self._get_positions(obj)
        return MapPositionSerializer(positions, many=True).data

    def _get_connections(self, obj):
        # Fetch connections related to the map positions
        positions = self._get_positions(obj).values_list('position', flat=True)
        connections = PositionConnection.objects.filter(
            position_from__in=positions, position_to__in=positions
        )
        return connections

    def get_connections(self, obj):
        # Fetch connections related to the map positions
        connections = self._get_connections(obj)
        return PositionConnectionMinimalSerializer(connections, many=True).data

    def _get_characters(self, obj):
        return obj.organization.character_set.all()

    def get_characters(self, obj):
        # Fetch characters related to the map's organization
        characters = self._get_characters(obj)
        return CharacterPositionSerializer(characters, many=True).data


class MiniMapSerializer(MapSerializer):

    def _get_positions(self, obj):
        return obj.map_positions.filter(
            is_active=True,
            position__grid_z=self._get_current_character().position.grid_z
        )

    def _get_characters(self, obj):
        return obj.organization.character_set.filter(
            position__grid_z=self._get_current_character().position.grid_z
        )
