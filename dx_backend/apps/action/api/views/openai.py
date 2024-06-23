from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.game.services.player.core import PlayerService
from ..serializers.openapi import PlayerActionSerializer
from ...models import PlayerAction


class PlayerActionsViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.GenericViewSet
):

    queryset = PlayerAction.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=1),
    )
    serializer_class = PlayerActionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        player = user.player
        qs = super().get_queryset()
        return qs.filter(initiator=player) | qs.filter(target=player)

    @transaction.atomic
    def perform_create(self, serializer):
        player1_service = PlayerService(self.request.user.player)
        # TODO: validate and execute Action, Looks we need action service

        return super().perform_create(serializer)

