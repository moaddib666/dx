from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.character.api.filters.character import CharacterFilter
from apps.character.api.serializers.openapi import CharacterInfoSerializer, CharacterStatsSerializer
from apps.character.models import Character
from apps.game.services.character.core import CharacterService
from apps.gamemaster.api.serializers.character import GameMasterCharacterInfoSerializer, GameMasterCharacterStatsCardSerializer


class GameMasterCharacterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for game masters to manage characters.
    This viewset provides full CRUD operations for characters.
    """
    queryset = Character.objects.filter(is_active=True)
    serializer_class = CharacterInfoSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CharacterFilter

    @action(detail=True, methods=['get'])
    def character_info(self, request, pk=None):
        """
        Get detailed information about a character.
        """
        try:
            character = self.get_object()
            service = CharacterService(character)
            character_info = service.get_character_info()
            return Response(data=character_info.model_dump())
        except Character.DoesNotExist:
            return Response({"detail": "Character not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], serializer_class=CharacterStatsSerializer)
    def character_stats(self, request, pk=None):
        """
        Get character stats.
        """
        try:
            character = self.get_object()
            serializer = self.get_serializer(character)
            return Response(data=serializer.data)
        except Character.DoesNotExist:
            return Response({"detail": "Character not found."}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        description="Get character information for the GameMasterCharacterCard component",
        responses={200: GameMasterCharacterInfoSerializer}
    )
    @action(detail=True, methods=['get'], serializer_class=GameMasterCharacterInfoSerializer)
    def character_card(self, request, pk=None):
        """
        Get character information for the GameMasterCharacterCard component.

        This endpoint provides all the necessary data for rendering a GameMasterCharacterCard,
        including character attributes, shields, active effects, equipped items, and currency.
        """
        try:
            character = self.get_object()
            serializer = self.get_serializer(character)
            return Response(data=serializer.data)
        except Character.DoesNotExist:
            return Response({"detail": "Character not found."}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        description="Get character stats for the GameMasterCharacterStatsCard component",
        responses={200: GameMasterCharacterStatsCardSerializer}
    )
    @action(detail=True, methods=['get'], serializer_class=GameMasterCharacterStatsCardSerializer)
    def character_stats_card(self, request, pk=None):
        """
        Get character stats for the GameMasterCharacterStatsCard component.

        This endpoint provides the necessary stats data for rendering a GameMasterCharacterStatsCard,
        including all character stats.
        """
        try:
            character = self.get_object()
            serializer = self.get_serializer(character)
            return Response(data=serializer.data)
        except Character.DoesNotExist:
            return Response({"detail": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
