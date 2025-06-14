from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.effects.api.serializers.openapi import (
    EffectSerializer, ActiveEffectSerializer
)
from apps.effects.models import Effect, ActiveEffect


class GameMasterEffectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage effects.
    This viewset provides full CRUD operations for effects.
    """
    queryset = Effect.objects.all()
    serializer_class = EffectSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterActiveEffectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage active effects.
    This viewset provides full CRUD operations for active effects.
    """
    queryset = ActiveEffect.objects.unsafe_all()
    serializer_class = ActiveEffectSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]