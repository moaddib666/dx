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
from rest_framework import viewsets, permissions, filters

from apps.knowledge_base.models import Document
from apps.knowledge_base.api.filters import DocumentFilter
from apps.knowledge_base.api.serializers import DocumentSerializer


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
