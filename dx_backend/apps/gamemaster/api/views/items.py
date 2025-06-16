from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from apps.gamemaster.api.serializers.item import GameMasterItemSerializer
from apps.items.api.serializers.openapi import (
    ItemSerializer, WorldItemSerializer, CharacterItemSerializer
)
from apps.items.models import Item, WorldItem, CharacterItem


class GameMasterItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for game masters to manage items.
    This viewset provides full CRUD operations for items.
    """
    queryset = Item.objects.all()
    serializer_class = GameMasterItemSerializer
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
