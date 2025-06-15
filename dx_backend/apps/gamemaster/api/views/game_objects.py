"""
The GameObjectViewSet provides endpoints for managing game objects.
GameObjects - this is a base class for all game objects in the game, such as characters, items, etc.
We use Django Polymorphic to handle different types of game objects.
We use Django REST Framework to create API endpoints for these objects.

This ViewSet implements:
1. List all game objects, output includes GameObject fields + Type for filtering by type.
2. Move GameObject to another position in the game world.
3. Delete GameObject.
4. Clone GameObject.
5. Disable/Enable GameObject.
"""

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.models import GameObject
from apps.gamemaster.api.filters import GameObjectFilter
from apps.gamemaster.api.serializers import GameObjectSerializer


class GameObjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage game objects.
    This viewset provides operations for listing, retrieving, creating, updating, and deleting game objects.
    It also provides custom actions for moving, cloning, and disabling/enabling game objects.
    """
    queryset = GameObject.objects.all()
    serializer_class = GameObjectSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = GameObjectFilter
    ordering_fields = ['id', 'is_active']


    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        """
        Move a game object to a new position.
        """
        game_object = self.get_object()
        position_id = request.data.get('position_id')

        if not position_id:
            return Response(
                {"error": "Position ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from apps.world.models import Position
            position = Position.objects.get(id=position_id)
            game_object.position = position
            game_object.save()
            return Response(self.get_serializer(game_object).data)
        except Position.DoesNotExist:
            return Response(
                {"error": "Position not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def clone(self, request, pk=None):
        """
        Clone a game object.
        """
        game_object = self.get_object()

        try:
            with transaction.atomic():
                # Get the actual polymorphic instance
                real_instance = game_object.get_real_instance()

                # Remove the primary key to create a new instance
                real_instance.pk = None
                real_instance.save()

                return Response(
                    self.get_serializer(real_instance).data,
                    status=status.HTTP_201_CREATED
                )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """
        Toggle the active status of a game object.
        """
        game_object = self.get_object()
        game_object.is_active = not game_object.is_active
        game_object.save()

        return Response(self.get_serializer(game_object).data)
