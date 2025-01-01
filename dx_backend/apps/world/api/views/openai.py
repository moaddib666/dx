from django.db import transaction
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.character.models import Character
from apps.core.api.utils.character import GenericGameViewSet
from apps.game.services.location import LocationService
from apps.game.services.world.position import JsonDumper
from apps.world.api.serializers.openapi import LocationSerializer, AreaSerializer, CitySerializer, DimensionSerializer, \
    PositionSerializer, TeleportPositionSerializer, TeleportCoordinatesSerializer
from apps.world.models import Location, Area, City, Dimension, Position


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
