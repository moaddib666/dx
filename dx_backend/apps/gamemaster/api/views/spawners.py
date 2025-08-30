from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.gamemaster.api.serializers.spawners import (
    NPCGenericSpawnerSerializer,
    NPCSpawnerCreateSerializer,
    NPCSpawnerListSerializer, GenericSpawnerSerializer,
)
from apps.spawner.models import NPCSpawner


@extend_schema(
    description="API for managing spawners in DX world editor.",
    tags=["GM World Editor - All Spawners"],
)
class GameMasterSpawnerViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for managing all spawners in the Game Master API.

    Provides read-only access to spawners with filtering capabilities.
    """
    queryset = NPCSpawner.objects.select_related(
        'position__sub_location',
        'campaign',
        'dimension'
    ).all()
    serializer_class = GenericSpawnerSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'campaign',
        'position',
        'is_active',
        'dimension',
    ]

    def get_queryset(self):
        """
        Override to filter spawners by the current campaign if applicable.
        Also supports additional filtering via query parameters.
        """
        queryset = super().get_queryset()

        # Filter by current campaign if user has one
        if self.request.user.is_authenticated and hasattr(self.request.user, 'current_campaign'):
            if self.request.user.current_campaign:
                queryset = queryset.filter(campaign=self.request.user.current_campaign)
        return queryset


@extend_schema(
    description="API for managing spawners in DX world editor.",
    tags=["GM World Editor - NPC Spawners"],
)
class GameMasterNPCSpawnerViewSet(ModelViewSet):
    """
    ViewSet for managing NPC spawners in the Game Master API.
    
    Provides complete CRUD functionality for spawners with different
    serializers optimized for different operations.
    """
    queryset = NPCSpawner.objects.select_related(
        'position__sub_location',
        'character_template',
        'campaign',
        'dimension'
    ).all()
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'campaign',
        'position',
        'character_template',
        'is_active',
        'dimension',
    ]

    def get_serializer_class(self):
        """
        Return different serializers based on the action.
        """
        if self.action == 'create':
            return NPCSpawnerCreateSerializer
        elif self.action == 'list':
            return NPCSpawnerListSerializer
        else:
            return NPCGenericSpawnerSerializer

    def get_queryset(self):
        """
        Override to filter spawners by the current campaign if applicable.
        Also supports additional filtering via query parameters.
        """
        queryset = super().get_queryset()

        # Filter by current campaign if user has one
        if self.request.user.is_authenticated and hasattr(self.request.user, 'current_campaign'):
            if self.request.user.current_campaign:
                queryset = queryset.filter(campaign=self.request.user.current_campaign)
        return queryset

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activate a spawner.
        """
        spawner = self.get_object()
        spawner.is_active = True
        spawner.save()
        serializer = self.get_serializer(spawner)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Deactivate a spawner.
        """
        spawner = self.get_object()
        spawner.is_active = False
        spawner.save()
        serializer = self.get_serializer(spawner)
        return Response(serializer.data)
