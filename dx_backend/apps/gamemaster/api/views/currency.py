from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.currency.api.serializers.openapi import (
    CurrencyTokenSerializer, CharacterCurrencySerializer
)
from apps.currency.models import CurrencyToken, CharacterCurrency


class GameMasterCurrencyTokenViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage currency tokens.
    This viewset provides full CRUD operations for currency tokens.
    """
    queryset = CurrencyToken.objects.all()
    serializer_class = CurrencyTokenSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterCharacterCurrencyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage character currencies.
    This viewset provides full CRUD operations for character currencies.
    """
    queryset = CharacterCurrency.objects.all()
    serializer_class = CharacterCurrencySerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]