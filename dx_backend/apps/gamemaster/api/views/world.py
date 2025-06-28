"""
The WorldMapViewSet must provide the following functionality:
TODO:
 Give positions in the world map filtered by the grid_z
 Give position connections in the world map filtered by the grid_z
 Give opportunities to crete new positions if provided nearby positions automatically connect them
 Give opportunities to create delete positions and connections (if delete position then delete all connections with it)
 Give opportunities to create new connections between positions
 Make possible to lock connections so players can't move through them
 As a result i as a game master can create world map with positions and connections between them and effectively manage it
"""

from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status, filters, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.gamemaster.api.serializers.world import PositionSerializer, PositionConnectionSerializer, \
    GridZParameterSerializer, MapResponseSerializer, PositionMoveSerializer, PositionConnectionCreateSerializer
from apps.world.api.serializers.openapi import PositionRelationConfigurationSerializer
from apps.world.models import Position, PositionConnection
from apps.game.services.world.position_connection import PositionConnectionService


class WorldMapViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage the world map.

    This viewset provides operations for:
    - Listing, retrieving, creating, updating, and deleting positions
    - Filtering positions by grid_z
    - Managing position connections
    - Creating positions with automatic connections to nearby positions
    - Locking/unlocking connections
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['grid_z', 'sub_location', 'is_safe']
    ordering_fields = ['grid_x', 'grid_y', 'grid_z']

    def get_queryset(self):
        """
        Get the list of positions, optionally filtered by grid_z.
        """
        queryset = super().get_queryset()
        grid_z = self.request.query_params.get('grid_z')
        if grid_z is not None:
            queryset = queryset.filter(grid_z=grid_z)
        return queryset

    def perform_destroy(self, instance):
        """
        Delete a position and all its connections.
        """
        with transaction.atomic():
            # Delete all connections associated with this position
            PositionConnection.objects.filter(
                Q(position_from=instance) | Q(position_to=instance)
            ).delete()
            # Delete the position
            instance.delete()

    @extend_schema(parameters=[GridZParameterSerializer])
    @action(detail=False, methods=['get'])
    def connections(self, request):
        """
        Get all position connections, optionally filtered by grid_z.
        """
        grid_z = request.query_params.get('grid_z')

        if grid_z is not None:
            # Filter connections where either position_from or position_to has the specified grid_z
            connections = PositionConnection.objects.filter(
                Q(position_from__grid_z=grid_z) | Q(position_to__grid_z=grid_z)
            )
        else:
            connections = PositionConnection.objects.all()

        serializer = PositionConnectionSerializer(connections, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_connection(self, request):
        """
        Create a new connection between two positions.
        """
        position_from_id = request.data.get('position_from')
        position_to_id = request.data.get('position_to')

        if not position_from_id:
            return Response(
                {"error": "position_from is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not position_to_id:
            return Response(
                {"error": "position_to is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            position_from = Position.objects.get(id=position_from_id)
            position_to = Position.objects.get(id=position_to_id)

            # Check if connection already exists
            existing_connection = PositionConnection.objects.filter(
                Q(position_from=position_from, position_to=position_to) |
                Q(position_from=position_to, position_to=position_from)
            ).first()

            if existing_connection:
                return Response(
                    {"error": "Connection already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create new connection
            connection = PositionConnection.objects.create(
                position_from=position_from,
                position_to=position_to,
                locked=request.data.get('locked', False),
                is_active=request.data.get('is_active', True),
                is_public=request.data.get('is_public', True)
            )

            serializer = PositionConnectionSerializer(connection)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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

    @action(detail=False, methods=['post'])
    def create_position_with_connections(self, request):
        """
        Create a new position and automatically connect it to nearby positions.
        """
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Create the new position
                position = serializer.save()

                # Find nearby positions (adjacent in any direction)
                nearby_positions = Position.objects.filter(
                    Q(grid_x=position.grid_x + 1, grid_y=position.grid_y, grid_z=position.grid_z) |
                    Q(grid_x=position.grid_x - 1, grid_y=position.grid_y, grid_z=position.grid_z) |
                    Q(grid_x=position.grid_x, grid_y=position.grid_y + 1, grid_z=position.grid_z) |
                    Q(grid_x=position.grid_x, grid_y=position.grid_y - 1, grid_z=position.grid_z) |
                    Q(grid_x=position.grid_x, grid_y=position.grid_y, grid_z=position.grid_z + 1) |
                    Q(grid_x=position.grid_x, grid_y=position.grid_y, grid_z=position.grid_z - 1)
                )

                # Create connections to nearby positions
                connections = []
                for nearby_position in nearby_positions:
                    connection = PositionConnection.objects.create(
                        position_from=position,
                        position_to=nearby_position,
                        locked=False,
                        is_active=True,
                        is_public=True
                    )
                    connections.append(connection)

                # Return the created position and its connections
                connection_serializer = PositionConnectionSerializer(connections, many=True)
                return Response({
                    'position': serializer.data,
                    'connections': connection_serializer.data
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def toggle_connection_lock(self, request, pk=None):
        """
        Lock or unlock a connection between this position and another position.
        """
        position = self.get_object()
        position_to_id = request.data.get('position_to')

        if not position_to_id:
            return Response(
                {"error": "position_to is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Find the connection
            connection = PositionConnection.objects.filter(
                Q(position_from=position, position_to_id=position_to_id) |
                Q(position_from_id=position_to_id, position_to=position)
            ).first()

            if not connection:
                return Response(
                    {"error": "Connection not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Toggle the lock status
            connection.locked = not connection.locked
            connection.save()

            serializer = PositionConnectionSerializer(connection)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['delete'])
    def delete_connection(self, request, pk=None):
        """
        Delete a connection between this position and another position.
        """
        position = self.get_object()
        position_to_id = request.query_params.get('position_to')

        if not position_to_id:
            return Response(
                {"error": "position_to is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Find the connection
            connection = PositionConnection.objects.filter(
                Q(position_from=position, position_to_id=position_to_id) |
                Q(position_from_id=position_to_id, position_to=position)
            ).first()

            if not connection:
                return Response(
                    {"error": "Connection not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Delete the connection
            connection.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(parameters=[GridZParameterSerializer], responses={200: MapResponseSerializer})
    @action(detail=False, methods=['get'])
    def map(self, request):
        """
        Get a complete map structure with positions and connections filtered by grid_z.
        """
        grid_z = request.query_params.get('grid_z')

        # Get positions filtered by grid_z
        if grid_z is not None:
            positions = Position.objects.filter(grid_z=grid_z)
        else:
            positions = Position.objects.all()

        # Get connections where either position_from or position_to has the specified grid_z
        if grid_z is not None:
            connections = PositionConnection.objects.filter(
                Q(position_from__grid_z=grid_z) | Q(position_to__grid_z=grid_z)
            )
        else:
            connections = PositionConnection.objects.all()

        # Serialize the data
        position_serializer = PositionSerializer(positions, many=True)
        connection_serializer = PositionConnectionSerializer(connections, many=True)

        # Return the combined data
        return Response({
            'positions': position_serializer.data,
            'connections': connection_serializer.data
        })


@extend_schema(
    description="API for managing positions in the world",
    tags=["GM World Editior - Positions"]
)
class PositionManagementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing positions via game master API.

    Provides CRUD operations for positions and additional actions for marking positions as safe/dangerous
    and moving positions to new coordinates.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['grid_z', 'sub_location', 'is_safe']
    ordering_fields = ['grid_x', 'grid_y', 'grid_z']

    @extend_schema(
        description="Mark a position as safe",
        responses={200: PositionSerializer}
    )
    @action(detail=True, methods=['post'])
    def markSafe(self, request, pk=None):
        """Mark a position as safe."""
        position = self.get_object()
        position.is_safe = True
        position.save()
        serializer = self.get_serializer(position)
        return Response(serializer.data)

    @extend_schema(
        description="Mark a position as dangerous",
        responses={200: PositionSerializer}
    )
    @action(detail=True, methods=['post'])
    def markDangerous(self, request, pk=None):
        """Mark a position as dangerous."""
        position = self.get_object()
        position.is_safe = False
        position.save()
        serializer = self.get_serializer(position)
        return Response(serializer.data)

    @extend_schema(
        description="Move a position to new coordinates",
        request=PositionMoveSerializer,
        responses={200: PositionSerializer}
    )
    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        """Move a position to new coordinates."""
        position = self.get_object()

        # Validate input
        grid_x = request.data.get('grid_x')
        grid_y = request.data.get('grid_y')
        grid_z = request.data.get('grid_z')

        if grid_x is None or grid_y is None or grid_z is None:
            return Response(
                {"error": "grid_x, grid_y, and grid_z are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the new coordinates are already taken
        if Position.objects.filter(
                grid_x=grid_x, grid_y=grid_y, grid_z=grid_z
        ).exclude(id=position.id).exists():
            return Response(
                {"error": "Position with these coordinates already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update position coordinates
        position.grid_x = grid_x
        position.grid_y = grid_y
        position.grid_z = grid_z
        position.save()

        serializer = self.get_serializer(position)
        return Response(serializer.data)


@extend_schema(
    description="API for managing position connections in the world",
    tags=["GM World Editior - Position Connections"]
)
class PositionConnectionManagementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing position connections.

    Provides CRUD operations for position connections and additional actions for locking/unlocking,
    activating/deactivating, setting public/private status, and configuring connections.
    """
    queryset = PositionConnection.objects.all()
    serializer_class = PositionConnectionSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_public']
    ordering_fields = ['position_from', 'position_to']

    @extend_schema(
        description="Lock a connection",
        responses={200: PositionConnectionSerializer}
    )
    @action(detail=True, methods=['post'])
    def lock(self, request, pk=None):
        """Lock a connection to prevent player movement."""
        connection = self.get_object()
        connection.locked = True
        connection.save()
        serializer = self.get_serializer(connection)
        return Response(serializer.data)

    @extend_schema(
        description="Unlock a connection",
        responses={200: PositionConnectionSerializer}
    )
    @action(detail=True, methods=['post'])
    def unlock(self, request, pk=None):
        """Unlock a connection to allow player movement."""
        connection = self.get_object()
        connection.locked = False
        connection.save()
        serializer = self.get_serializer(connection)
        return Response(serializer.data)

    @extend_schema(
        description="Configure a connection with requirements",
        request=PositionRelationConfigurationSerializer,
        responses={200: PositionConnectionSerializer}
    )
    @action(detail=True, methods=['post'])
    def configure(self, request, pk=None):
        """Configure a connection with specific requirements."""
        connection = self.get_object()

        # Validate the configuration data
        config_serializer = PositionRelationConfigurationSerializer(data=request.data)
        if not config_serializer.is_valid():
            return Response(config_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use the service to parse and validate the configuration
            connection_service = PositionConnectionService(connection)

            # Update the connection configuration
            connection.config = config_serializer.validated_data
            connection.save()

            serializer = self.get_serializer(connection)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(
        description="Deactivate a connection",
        responses={200: PositionConnectionSerializer}
    )
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a connection."""
        connection = self.get_object()
        connection.is_active = False
        connection.save()
        serializer = self.get_serializer(connection)
        return Response(serializer.data)

    @extend_schema(
        description="Activate a connection",
        responses={200: PositionConnectionSerializer}
    )
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a connection."""
        connection = self.get_object()
        connection.is_active = True
        connection.save()
        serializer = self.get_serializer(connection)
        return Response(serializer.data)

    @extend_schema(
        description="Set a connection as public",
        responses={200: PositionConnectionSerializer}
    )
    @action(detail=True, methods=['post'])
    def setPublic(self, request, pk=None):
        """Set a connection as public."""
        connection = self.get_object()
        connection.is_public = True
        connection.save()
        serializer = self.get_serializer(connection)
        return Response(serializer.data)

    @extend_schema(
        description="Set a connection as private",
        responses={200: PositionConnectionSerializer}
    )
    @action(detail=True, methods=['post'])
    def setPrivate(self, request, pk=None):
        """Set a connection as private."""
        connection = self.get_object()
        connection.is_public = False
        connection.save()
        serializer = self.get_serializer(connection)
        return Response(serializer.data)

    @extend_schema(
        description="Create a connection between two positions",
        request=PositionConnectionCreateSerializer,
        responses={201: PositionConnectionSerializer}
    )
    @action(detail=False, methods=['post'])
    def connect(self, request):
        """Create a connection between two positions."""
        position_from_id = request.data.get('position_from')
        position_to_id = request.data.get('position_to')

        if not position_from_id or not position_to_id:
            return Response(
                {"error": "position_from and position_to are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            position_from = Position.objects.get(id=position_from_id)
            position_to = Position.objects.get(id=position_to_id)

            # Check if connection already exists
            if PositionConnection.objects.filter(
                    position_from=position_from, position_to=position_to
            ).exists() or PositionConnection.objects.filter(
                position_from=position_to, position_to=position_from
            ).exists():
                return Response(
                    {"error": "Connection already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create new connection
            connection = PositionConnection.objects.create(
                position_from=position_from,
                position_to=position_to,
                locked=request.data.get('locked', False),
                is_active=request.data.get('is_active', True),
                is_public=request.data.get('is_public', True)
            )

            serializer = self.get_serializer(connection)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Position.DoesNotExist:
            return Response(
                {"error": "Position not found"},
                status=status.HTTP_404_NOT_FOUND
            )
