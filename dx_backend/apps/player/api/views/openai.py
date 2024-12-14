from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.game.services.player import PlayerFactory
from apps.game.services.player.core import PlayerService
from apps.player.api.serializers.openapi import OpenaiCharacterSerializer, PlayerInfoSerializer, PlayerPathSerializer
from apps.player.models import Player


class OpenAISchoolsManagementViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.filter(is_active=True)
    serializer_class = OpenaiCharacterSerializer
    permission_classes = [permissions.IsAdminUser]

    # TODO move TO THE GAME SETTINGS
    PLAYER_CREATION_LIMIT = 5

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs
        return Player.objects.filter(owner=user)

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user

        # Check the limit
        current_player_count = Player.objects.filter(owner=user).count()
        if current_player_count >= self.PLAYER_CREATION_LIMIT:
            return Response(
                {'detail': f'Player creation limit of {self.PLAYER_CREATION_LIMIT} reached.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        factory = PlayerFactory(user)
        player = factory.create_player(
            name=serializer.validated_data['name'],
            age=serializer.validated_data['age'],
            gender=serializer.validated_data['gender'],
        )
        serializer.instance = player

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated],
            serializer_class=PlayerInfoSerializer)
    def player_info(self, request):
        user = request.user
        try:
            player = user.player
            service = PlayerService(player)
            player_info = service.get_player_info()
            return Response(data=player_info.dict())
        except Player.DoesNotExist:
            return Response({"detail": "Player not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated], serializer_class=PlayerPathSerializer)
    def chose_path(self, request, pk=None):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            player = user.player
            service = PlayerService(player)
            service.chose_path(serializer.validated_data['path'])
            return Response({"detail": "Path chosen."})
        except Player.DoesNotExist:
            return Response({"detail": "Player not found."}, status=status.HTTP_404_NOT_FOUND)
