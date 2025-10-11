"""
The TimeLineEventViewSet provides endpoints for managing timeline events.

This ViewSet implements:
1. List all timeline events with filtering and pagination
2. Retrieve a single timeline event
3. Create a new timeline event
4. Update an existing timeline event
5. Delete a timeline event
6. Import action for bulk import with nested Document and DateTimeInfo
"""

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.knowledge_base.models import TimeLineEvent
from apps.knowledge_base.api.filters import TimeLineEventFilter
from apps.knowledge_base.api.serializers import (
    TimeLineEventSerializer,
    TimeLineEventImportSerializer,
)


class TimeLineEventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing timeline events.
    This viewset provides operations for listing, retrieving, creating, updating, and deleting timeline events.
    Supports filtering by document, date_time, and date_time fields, as well as ordering and pagination.
    
    Permissions:
    - Read operations (GET, LIST): Allowed for all users
    - Write operations (POST, PUT, PATCH, DELETE): Restricted to admin users only
    """
    queryset = TimeLineEvent.objects.select_related('document', 'date_time').all()
    serializer_class = TimeLineEventSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = TimeLineEventFilter
    ordering_fields = ['id', 'created_at', 'updated_at', 'date_time__solar_year', 'date_time__sol']
    ordering = ['date_time__solar_year', 'date_time__sol']  # Default ordering by timeline
    search_fields = ['document__title', 'document__content']
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        - Read operations (list, retrieve): Allow any user
        - Write operations (create, update, partial_update, destroy): Require admin user
        - Import action: Require admin user
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @extend_schema(
        request=TimeLineEventImportSerializer,
        responses={201: TimeLineEventSerializer},
        description="Import a timeline event with nested Document and DateTimeInfo. "
                    "This action will get_or_create Document and DateTimeInfo, then create the TimeLineEvent. "
                    "Image loading is not supported in this action."
    )
    @action(detail=False, methods=['post'])
    def import_event(self, request):
        """
        Import a timeline event with nested Document and DateTimeInfo.
        
        This action accepts a JSON payload with full Document and DateTimeInfo data.
        It will:
        1. Get or create the Document based on title and content
        2. Get or create the DateTimeInfo based on active_glow, sol, and solar_year
        3. Create a new TimeLineEvent linking them together
        
        Example payload:
        {
            "document": {
                "title": "The Great Battle",
                "content": "A historic battle that changed everything...",
                "categories": ["events", "lore"]
            },
            "date_time": {
                "active_glow": true,
                "sol": 150,
                "solar_year": 42
            }
        }
        """
        serializer = TimeLineEventImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        timeline_event = serializer.save()
        
        # Return the created timeline event using the standard serializer
        output_serializer = TimeLineEventSerializer(timeline_event)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
