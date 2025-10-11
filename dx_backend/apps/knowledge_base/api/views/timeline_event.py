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
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.knowledge_base.models import TimeLineEvent
from apps.knowledge_base.api.filters import TimeLineEventFilter
from apps.knowledge_base.api.serializers import (
    TimeLineEventSerializer,
    TimeLineEventImportSerializer,
)
from apps.knowledge_base.api.pagination import KnowledgeBasePagination


@extend_schema_view(
    list=extend_schema(
        summary="List all timeline events",
        description="Retrieve a paginated list of all timeline events. "
                    "Supports filtering by document, active_glow, solar_year, and sol. "
                    "Supports searching across document title and content. "
                    "Default ordering is by timeline (solar_year, sol).",
        tags=["Knowledge Base - Timeline Events"],
        parameters=[
            OpenApiParameter(name='document', description='Filter by document ID', required=False, type=str),
            OpenApiParameter(name='date_time', description='Filter by date_time ID', required=False, type=str),
            OpenApiParameter(name='active_glow', description='Filter by active_glow (true/false)', required=False, type=bool),
            OpenApiParameter(name='solar_year', description='Filter by exact solar year', required=False, type=int),
            OpenApiParameter(name='sol_gte', description='Filter by sol greater than or equal to value', required=False, type=int),
            OpenApiParameter(name='search', description='Search across document title and content', required=False, type=str),
            OpenApiParameter(name='ordering', description='Order results by field (prefix with - for descending)', required=False, type=str),
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve a timeline event",
        description="Retrieve detailed information about a specific timeline event by its ID. "
                    "Includes related document and date_time information.",
        tags=["Knowledge Base - Timeline Events"],
    ),
    create=extend_schema(
        summary="Create a new timeline event",
        description="Create a new timeline event. Requires admin privileges. "
                    "You must provide existing document_id and date_time_id.",
        tags=["Knowledge Base - Timeline Events"],
    ),
    update=extend_schema(
        summary="Update a timeline event",
        description="Update all fields of an existing timeline event. Requires admin privileges.",
        tags=["Knowledge Base - Timeline Events"],
    ),
    partial_update=extend_schema(
        summary="Partially update a timeline event",
        description="Update specific fields of an existing timeline event. Requires admin privileges.",
        tags=["Knowledge Base - Timeline Events"],
    ),
    destroy=extend_schema(
        summary="Delete a timeline event",
        description="Delete a timeline event. Requires admin privileges. "
                    "Note: This does not delete the associated document or date_time records.",
        tags=["Knowledge Base - Timeline Events"],
    ),
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
    pagination_class = KnowledgeBasePagination
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
        summary="Import timeline event with nested data",
        request=TimeLineEventImportSerializer,
        responses={201: TimeLineEventSerializer},
        description="Import a timeline event with nested Document and DateTimeInfo data. "
                    "This action will get_or_create Document and DateTimeInfo based on the provided data, "
                    "then create the TimeLineEvent linking them together. "
                    "This is useful for bulk imports or migrations. "
                    "Note: Image loading is not supported in this action.",
        tags=["Knowledge Base - Timeline Events"],
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
