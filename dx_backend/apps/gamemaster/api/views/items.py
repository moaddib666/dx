from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.items.api.serializers.openapi import (
    ItemSerializer, WorldItemSerializer, CharacterItemSerializer
)
from apps.items.models import Item, WorldItem, CharacterItem


class GameMasterItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage items.
    This viewset provides full CRUD operations for items.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterWorldItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage world items.
    This viewset provides full CRUD operations for world items.
    """
    queryset = WorldItem.objects.all()
    serializer_class = WorldItemSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterCharacterItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage character items.
    This viewset provides full CRUD operations for character items.
    """
    queryset = CharacterItem.objects.all()
    serializer_class = CharacterItemSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]