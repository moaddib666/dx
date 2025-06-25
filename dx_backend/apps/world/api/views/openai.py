from django.db import transaction
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from apps.character.models import Character
from apps.core.api.utils.character import GenericGameViewSet
from apps.core.models import ItemType
from apps.core.utils.api import CampaignFilterMixin
from apps.game.services.location import LocationService
from apps.game.services.world.position import JsonDumper
from apps.world.api.serializers.openapi import LocationSerializer, AreaSerializer, CitySerializer, DimensionSerializer, \
    PositionSerializer, TeleportPositionSerializer, TeleportCoordinatesSerializer, MapPositionSerializer, \
    NewCoordinatesSerializer, MapSerializer, GenericPositionSerializer, GenericPositionIdSerializer, \
    MapPositionMutableSerializer, MiniMapSerializer
from apps.world.models import Location, Area, City, Dimension, Position, MapPosition, Map


class OpenAICityManagementViewSet(viewsets.ReadOnlyModelViewSet, GenericGameViewSet):
    queryset = City.objects.filter(is_active=True)
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs
        current_user_location = user.character.current_location
        aria = current_user_location.area
        city = aria.city
        return qs.filter(id__in=[city.id, *city.border_with.values_list('id', flat=True)])

    @action(detail=False, methods=['get'])
    def current(self, request):
        user = request.user
        current_user_location = user.main_character.current_location
        aria = current_user_location.area
        city = aria.city
        data = CitySerializer(city).data
        return Response(data)


class OpenAILocationManagementViewSet(viewsets.ReadOnlyModelViewSet, GenericGameViewSet):
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs
        current_user_location = user.character.current_location
        return qs.filter(
            id__in=[current_user_location.id, *current_user_location.border_with.values_list('id', flat=True)])

    @action(detail=False, methods=['get'])
    def current(self, request):
        character = self.get_character()
        current_user_location = character.current_location
        data = LocationSerializer(current_user_location).data
        return Response(data)

    @action(detail=True, methods=['post'], serializer_class=None, permission_classes=[permissions.IsAuthenticated], )
    def change(self, request, pk=None):
        character = self.get_character()
        new_location = self.get_object()
        service = LocationService()
        service.change_character_location(character, new_location)
        return Response(data=LocationSerializer(new_location).data)


class OpenAIAreaManagementViewSet(viewsets.ReadOnlyModelViewSet, GenericGameViewSet):
    queryset = Area.objects.filter(is_active=True)
    serializer_class = AreaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs
        current_user_location = user.character.current_location
        aria = current_user_location.area
        return qs.filter(id__in=[aria.id, *aria.border_with.values_list('id', flat=True)])

    @action(detail=False, methods=['get'])
    def current(self, request):
        user = request.user
        current_user_location = user.main_character.current_location
        aria = current_user_location.area
        data = AreaSerializer(aria).data
        return Response(data)


class OpenAIDimensionManagementViewSet(viewsets.ReadOnlyModelViewSet, GenericGameViewSet):
    queryset = Dimension.objects.filter(is_active=True)
    serializer_class = DimensionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs
        character = user.character
        current_user_dimension = character.dimension

        return qs.filter(
            id__in=[current_user_dimension.id, current_user_dimension + 1, current_user_dimension - 1],
            grade__lte=character.rank_grade.grade
        )

    @action(detail=False, methods=['get'])
    def current(self, request):
        character = self.get_character()
        current_user_dimension = character.dimension
        data = DimensionSerializer(current_user_dimension).data
        return Response(data)


class PositionManagementViewSet(GenericGameViewSet):
    queryset = Character.objects.filter(is_active=True)
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        Return the current position of the character and possible movements.
        """
        #   {
        #     "location": uuid,
        #     "sub_location": uuid,
        #     "position": uuid,
        #     "characters": [ uuid, uuid, ... ],
        #     "connections": [
        #         {
        #             "direction": "NORTH",
        #             "position": uuid
        #         },
        #         {
        #             "direction": "SOUTH",
        #             "position": uuid
        #         },
        #         ...]
        #
        # }
        #
        #  # "gameobjects": [ uuid, uuid, ... ] # TODO: implement game objects id, type, interface

        character = self.get_character()  # Assume this fetches the character
        position = character.position  # Assume the character has a related Position object

        # Serialize the position details
        serializer = self.get_serializer(position, context=self.get_serializer_context())
        return Response(data=serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def info(self, request, pk=None):
        pos = get_object_or_404(Position, pk=pk)
        serializer = PositionSerializer(pos, context=self.get_serializer_context())
        return Response(data=serializer.data)

    @action(detail=True, methods=['post'], serializer_class=None, permission_classes=[permissions.IsAuthenticated])
    def move_to_position(self, request, pk=None):
        character = self.get_character()
        new_position = Position.objects.get(pk=pk)

        # Validata the movement
        # Schedule the movement to be executed in when turn ends

        character.position = new_position
        character.save()
        return Response(data=PositionSerializer(new_position, context=self.get_serializer_context()).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser],
            serializer_class=TeleportPositionSerializer)
    @transaction.atomic
    def teleport_to_position(self, request, pk=None):
        char = self.get_object()
        serializer = TeleportPositionSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        char.position = serializer.save()
        char.save()
        return Response(data=serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser],
            serializer_class=TeleportCoordinatesSerializer)
    @transaction.atomic
    def teleport_to_coordinates(self, request, pk=None):
        char = self.get_object()
        serializer = TeleportCoordinatesSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        char.position = serializer.save()
        char.save()
        return Response(data=serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def map(self, request):
        """
        Return the map of the current location.
        """
        svc = JsonDumper(None, context=self.get_serializer_context())
        return Response(data=svc.as_dict())


class MappedPositionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MapPosition.objects.all()
    serializer_class = MapPositionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> MapPosition.objects:
        user = self.request.user
        org = user.main_character.organization
        qs = super().get_queryset()
        return qs.filter(
            map__organization=org
        ).select_related('map', 'position')

    @extend_schema(request=NewCoordinatesSerializer, responses=MapPositionSerializer)
    @action(detail=False, methods=['post'], serializer_class=NewCoordinatesSerializer)
    def map_position(self, request):
        try:
            serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
            serializer.is_valid(raise_exception=True)
            allowed = Character.objects.filter(
                Q(position=serializer.instance)
                | Q(position__position_from__position_to=serializer.instance)
                | Q(position__position_to__position_from=serializer.instance),
                organization=self.request.user.main_character.organization).exists()
            if not allowed:
                raise ValueError("Position is not allowed to be mapped")
            new_mapped_position = self.get_queryset().create(
                map=self.request.user.main_character.organization.map,
                position=serializer.instance,
                labels=serializer.data.get('labels', [])
            )
        except Exception as err:
            raise serializers.ValidationError(
                "Position invalid or not discovered yet"
            ) from err

        return Response(data=MapPositionSerializer(new_mapped_position).data)


class HasCartographerItem(IsAuthenticated):
    """
    Allows access only to users with cartographer item.
    """
    def has_permission(self, request, view):
        auth = super().has_permission(request, view)
        if not auth:
            return False
        character = request.user.main_character
        return Character.objects.filter(
            equipped_items__world_item__item__type=ItemType.QUEST,
            equipped_items__world_item__item__name='Cartograph'
        ).distinct().filter(id=character.id).exists()


class MapViewSet(viewsets.GenericViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    permission_classes = [HasCartographerItem, ]

    def get_queryset(self):
        user = self.request.user
        org = user.main_character.organization
        qs = super().get_queryset()
        return qs.filter(organization=org)

    def get_organization_map(self):
        try:
            user = self.request.user
            org = user.main_character.organization
            qs = self.get_queryset()
            return qs.get(organization=org)
        except Map.DoesNotExist:
            raise serializers.ValidationError("Organization map not found")

    @action(detail=False, methods=['get'])
    def world_map(self, request):
        """
        Return the world map of the current organization.
        """
        return Response(data=self.get_serializer(self.get_organization_map(), context=self.get_serializer_context()).data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], serializer_class=MiniMapSerializer)
    def mini_map(self, request):
        """
        Return the mini map of the current organization.
        """
        return Response(data=self.get_serializer(self.get_organization_map(), context=self.get_serializer_context()).data)

    @extend_schema(request=NewCoordinatesSerializer, responses=MapPositionSerializer)
    @action(detail=False, methods=['post'], serializer_class=NewCoordinatesSerializer)
    def position_add(self, request):
        try:
            serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
            serializer.is_valid(raise_exception=True)
            allowed = Character.objects.filter(
                Q(position=serializer.instance)
                | Q(position__position_from__position_to=serializer.instance)
                | Q(position__position_to__position_from=serializer.instance),
                organization=self.request.user.main_character.organization).exists()
            if not allowed:
                raise ValueError("Position is not allowed to be mapped")
            org_map = self.get_organization_map()
            position = org_map.map_positions.create(
                position=serializer.instance,
                labels=serializer.data.get('labels', [])
            )
        except Exception as err:
            raise serializers.ValidationError(
                "Position invalid or not discovered yet"
            ) from err

        return Response(data=MapPositionSerializer(position, context=self.get_serializer_context()).data)

    @action(detail=False, methods=['post'], serializer_class=GenericPositionIdSerializer)
    def position_remove(self, request):
        serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        org_map = self.get_organization_map()
        org_map.map_positions.filter(position=serializer.instance).delete()
        return Response(data=self.get_serializer(org_map, context=self.get_serializer_context()).data)

    @extend_schema(request=MapPositionMutableSerializer, responses=MapSerializer)
    @action(detail=False, methods=['post'], serializer_class=MapPositionMutableSerializer)
    def position_update(self, request):
        serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        org_map = self.get_organization_map()
        org_map.map_positions.filter(position_id=serializer.validated_data['position_id']).update(
            labels=serializer.validated_data['labels']
        )
        return Response(data=MapSerializer(self.get_organization_map(), context=self.get_serializer_context()).data)
