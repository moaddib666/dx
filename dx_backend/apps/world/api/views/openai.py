from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.api.utils.player import GenericGameViewSet
from apps.game.services.location import LocationService
from apps.player.models import Player
from apps.world.api.serializers.openapi import LocationSerializer, AreaSerializer, CitySerializer, DimensionSerializer, \
    PositionSerializer
from apps.world.models import Location, Area, City, Dimension


class OpenAICityManagementViewSet(viewsets.ReadOnlyModelViewSet, GenericGameViewSet):
    queryset = City.objects.filter(is_active=True)
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs
        current_user_location = user.player.current_location
        aria = current_user_location.area
        city = aria.city
        return qs.filter(id__in=[city.id, *city.border_with.values_list('id', flat=True)])

    @action(detail=False, methods=['get'])
    def current(self, request):
        user = request.user
        current_user_location = user.player.current_location
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
        current_user_location = user.player.current_location
        return qs.filter(id__in=[current_user_location.id, *current_user_location.border_with.values_list('id', flat=True)])

    @action(detail=False, methods=['get'])
    def current(self, request):
        player = self.get_player()
        current_user_location = player.current_location
        data = LocationSerializer(current_user_location).data
        return Response(data)

    @action(detail=True, methods=['post'], serializer_class=None, permission_classes=[permissions.IsAuthenticated],)
    def change(self, request, pk=None):
        player = self.get_player()
        new_location = self.get_object()
        service = LocationService()
        service.change_player_location(player, new_location)
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
        current_user_location = user.player.current_location
        aria = current_user_location.area
        return qs.filter(id__in=[aria.id, *aria.border_with.values_list('id', flat=True)])

    @action(detail=False, methods=['get'])
    def current(self, request):
        user = request.user
        current_user_location = user.player.current_location
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
        player = user.player
        current_user_dimension = player.dimension

        return qs.filter(
            id__in=[current_user_dimension.id, current_user_dimension+1, current_user_dimension-1],
            grade__lte=player.rank.grade
        )

    @action(detail=False, methods=['get'])
    def current(self, request):
        player = self.get_player()
        current_user_dimension = player.dimension
        data = DimensionSerializer(current_user_dimension).data
        return Response(data)


class PositionManagementViewSet(GenericGameViewSet):
    queryset = Player.objects.filter(is_active=True)
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def current(self, request):
        player = self.get_player()
        serializer = self.get_serializer(player)
        return Response(data=serializer.data)
