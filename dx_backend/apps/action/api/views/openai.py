from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.game.services.character.core import CharacterService
from ..serializers.openapi import CharacterActionSerializer
from ...models import CharacterAction


class CharacterActionsViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.GenericViewSet
):

    queryset = CharacterAction.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=1),
    )
    serializer_class = CharacterActionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        character = user.character
        qs = super().get_queryset()
        return qs.filter(initiator=character) | qs.filter(target=character)

    @transaction.atomic
    def perform_create(self, serializer):
        character1_service = CharacterService(self.request.user.character)
        # TODO: validate and execute Action, Looks we need action service

        return super().perform_create(serializer)

