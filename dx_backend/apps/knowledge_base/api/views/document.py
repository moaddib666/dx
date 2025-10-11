"""
The DocumentViewSet provides endpoints for managing knowledge base documents.

This ViewSet implements:
1. List all documents with filtering and pagination
2. Retrieve a single document
3. Create a new document
4. Update an existing document
5. Delete a document
"""

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, permissions, filters

from apps.knowledge_base.models import Document
from apps.knowledge_base.api.filters import DocumentFilter
from apps.knowledge_base.api.serializers import DocumentSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all documents",
        description="Retrieve a paginated list of all knowledge base documents. "
                    "Supports filtering by title, content, and categories. "
                    "Supports searching across title and content fields. "
                    "Supports ordering by id, title, created_at, and updated_at.",
        tags=["Knowledge Base - Documents"],
        parameters=[
            OpenApiParameter(name='title', description='Filter by title (case-insensitive partial match)', required=False, type=str),
            OpenApiParameter(name='content', description='Filter by content (case-insensitive partial match)', required=False, type=str),
            OpenApiParameter(name='categories', description='Filter by category name (exact match)', required=False, type=str),
            OpenApiParameter(name='search', description='Search across title and content fields', required=False, type=str),
            OpenApiParameter(name='ordering', description='Order results by field (prefix with - for descending)', required=False, type=str),
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve a document",
        description="Retrieve detailed information about a specific knowledge base document by its ID.",
        tags=["Knowledge Base - Documents"],
    ),
    create=extend_schema(
        summary="Create a new document",
        description="Create a new knowledge base document. Requires admin privileges. "
                    "You can optionally assign categories to the document.",
        tags=["Knowledge Base - Documents"],
    ),
    update=extend_schema(
        summary="Update a document",
        description="Update all fields of an existing knowledge base document. Requires admin privileges.",
        tags=["Knowledge Base - Documents"],
    ),
    partial_update=extend_schema(
        summary="Partially update a document",
        description="Update specific fields of an existing knowledge base document. Requires admin privileges.",
        tags=["Knowledge Base - Documents"],
    ),
    destroy=extend_schema(
        summary="Delete a document",
        description="Delete a knowledge base document. Requires admin privileges. "
                    "This will also delete all associated timeline events.",
        tags=["Knowledge Base - Documents"],
    ),
)
class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing knowledge base documents.
    This viewset provides operations for listing, retrieving, creating, updating, and deleting documents.
    Supports filtering by title, content, and categories, as well as ordering and pagination.
    
    Permissions:
    - Read operations (GET, LIST): Allowed for all users
    - Write operations (POST, PUT, PATCH, DELETE): Restricted to admin users only
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = DocumentFilter
    ordering_fields = ['id', 'title', 'created_at', 'updated_at']
    ordering = ['-created_at']  # Default ordering
    search_fields = ['title', 'content']
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        - Read operations (list, retrieve): Allow any user
        - Write operations (create, update, partial_update, destroy): Require admin user
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
