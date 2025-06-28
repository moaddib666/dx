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

from apps.gamemaster.api.serializers.world import PositionSerializer, PositionConnectionSerializer
from apps.world.models import Position, PositionConnection


class GridZParameterSerializer(serializers.Serializer):
    grid_z = serializers.IntegerField(required=False, help_text="Filter by grid_z coordinate")


class MapResponseSerializer(serializers.Serializer):
    """
    Response serializer for the map endpoint.
    """
    positions = PositionSerializer(many=True)
    connections = PositionConnectionSerializer(many=True)


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
                is_locked=request.data.get('is_locked', False),
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
                    Q(grid_x=position.grid_x+1, grid_y=position.grid_y, grid_z=position.grid_z) |
                    Q(grid_x=position.grid_x-1, grid_y=position.grid_y, grid_z=position.grid_z) |
                    Q(grid_x=position.grid_x, grid_y=position.grid_y+1, grid_z=position.grid_z) |
                    Q(grid_x=position.grid_x, grid_y=position.grid_y-1, grid_z=position.grid_z) |
                    Q(grid_x=position.grid_x, grid_y=position.grid_y, grid_z=position.grid_z+1) |
                    Q(grid_x=position.grid_x, grid_y=position.grid_y, grid_z=position.grid_z-1)
                )

                # Create connections to nearby positions
                connections = []
                for nearby_position in nearby_positions:
                    connection = PositionConnection.objects.create(
                        position_from=position,
                        position_to=nearby_position,
                        is_locked=False,
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
            connection.is_locked = not connection.is_locked
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
