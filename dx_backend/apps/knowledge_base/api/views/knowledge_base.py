from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.knowledge_base.models import KnowledgeBaseItem, KnowledgeBaseItemTag, DXDate
from apps.knowledge_base.api.serializers import (
    KnowledgeBaseItemSerializer,
    KnowledgeBaseItemTagSerializer,
    DXDateSerializer
)


class KnowledgeBaseItemTagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing knowledge base item tags.
    
    This viewset provides operations for:
    - Listing, retrieving, creating, updating, and deleting tags
    - Searching tags by label
    - Viewing tag usage statistics
    """
    queryset = KnowledgeBaseItemTag.objects.all()
    serializer_class = KnowledgeBaseItemTagSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['label']
    ordering_fields = ['label']
    ordering = ['label']

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """
        Get all knowledge base items associated with this tag.
        """
        tag = self.get_object()
        items = tag.knowledge_base_items.all()
        serializer = KnowledgeBaseItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        Get tags ordered by usage count (most popular first).
        """
        tags = self.get_queryset().annotate(
            usage_count=models.Count('knowledge_base_items')
        ).order_by('-usage_count')
        
        page = self.paginate_queryset(tags)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data)


class DXDateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing DX dates with cycle-based dating system.
    
    This viewset provides operations for:
    - Listing, retrieving, creating, updating, and deleting DX dates
    - Filtering by BAG (Before Active Glow) status
    - Ordering by cycle number
    - Era-Decade-Sol conversion utilities
    """
    queryset = DXDate.objects.all()
    serializer_class = DXDateSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['BAG']
    ordering_fields = ['dxCycle']
    ordering = ['dxCycle']

    @action(detail=False, methods=['get'])
    def cycle_range(self, request):
        """
        Get DX dates within a specific cycle range.
        Query parameters: start_cycle, end_cycle
        """
        start_cycle = request.query_params.get('start_cycle')
        end_cycle = request.query_params.get('end_cycle')
        
        if not start_cycle or not end_cycle:
            return Response(
                {'error': 'Both start_cycle and end_cycle parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_cycle = int(start_cycle)
            end_cycle = int(end_cycle)
        except ValueError:
            return Response(
                {'error': 'Cycle parameters must be integers'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        dates = self.get_queryset().filter(
            dxCycle__gte=start_cycle,
            dxCycle__lte=end_cycle
        )
        
        page = self.paginate_queryset(dates)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(dates, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def convert_era_decade_sol(self, request):
        """
        Convert Era-Decade-Sol format to dxCycle.
        Body: {"era": int, "decade": int, "sol": int, "cycle": int}
        """
        era = request.data.get('era', 0)
        decade = request.data.get('decade', 0)
        sol = request.data.get('sol', 0)
        cycle = request.data.get('cycle', 0)
        
        try:
            era = int(era)
            decade = int(decade)
            sol = int(sol)
            cycle = int(cycle)
        except (ValueError, TypeError):
            return Response(
                {'error': 'All parameters must be integers'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert to dxCycle: Era = 1000 Decade, Decade = 10 Sol, Sol = 100 cycles
        dx_cycle = (era * 1000 * 10 * 100) + (decade * 10 * 100) + (sol * 100) + cycle
        
        return Response({
            'dxCycle': dx_cycle,
            'input': {
                'era': era,
                'decade': decade,
                'sol': sol,
                'cycle': cycle
            }
        })


class KnowledgeBaseItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing knowledge base items (events, locations, characters).
    
    This viewset provides operations for:
    - Listing, retrieving, creating, updating, and deleting knowledge base items
    - Filtering by category, cycle range, tags
    - Searching by description and metadata
    - Managing breadcrumb relationships
    - Bulk operations for tags
    """
    queryset = KnowledgeBaseItem.objects.all()
    serializer_class = KnowledgeBaseItemSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['description', 'metadata']
    ordering_fields = ['dxCycle', 'category', 'created_at', 'updated_at']
    ordering = ['dxCycle', 'category']

    def get_queryset(self):
        """
        Optionally filter by cycle range and tags.
        """
        queryset = super().get_queryset()
        
        # Filter by cycle range
        start_cycle = self.request.query_params.get('start_cycle')
        end_cycle = self.request.query_params.get('end_cycle')
        
        if start_cycle:
            try:
                queryset = queryset.filter(dxCycle__gte=int(start_cycle))
            except ValueError:
                pass
        
        if end_cycle:
            try:
                queryset = queryset.filter(dxCycle__lte=int(end_cycle))
            except ValueError:
                pass
        
        # Filter by tags
        tags = self.request.query_params.get('tags')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            queryset = queryset.filter(tags__label__in=tag_list).distinct()
        
        return queryset

    @action(detail=True, methods=['get'])
    def breadcrumb_tree(self, request, pk=None):
        """
        Get the full breadcrumb tree for this item (parents and children).
        """
        item = self.get_object()
        
        # Get all breadcrumbs (parents)
        breadcrumbs = item.breadcrumbs.all()
        
        # Get all child items (items that have this as breadcrumb)
        children = item.child_items.all()
        
        return Response({
            'item': self.get_serializer(item).data,
            'breadcrumbs': self.get_serializer(breadcrumbs, many=True).data,
            'children': self.get_serializer(children, many=True).data
        })

    @action(detail=True, methods=['post'])
    def add_breadcrumb(self, request, pk=None):
        """
        Add a breadcrumb relationship to this item.
        Body: {"breadcrumb_id": "uuid"}
        """
        item = self.get_object()
        breadcrumb_id = request.data.get('breadcrumb_id')
        
        if not breadcrumb_id:
            return Response(
                {'error': 'breadcrumb_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            breadcrumb = KnowledgeBaseItem.objects.get(id=breadcrumb_id)
            item.breadcrumbs.add(breadcrumb)
            return Response({'status': 'Breadcrumb added successfully'})
        except KnowledgeBaseItem.DoesNotExist:
            return Response(
                {'error': 'Breadcrumb item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def remove_breadcrumb(self, request, pk=None):
        """
        Remove a breadcrumb relationship from this item.
        Body: {"breadcrumb_id": "uuid"}
        """
        item = self.get_object()
        breadcrumb_id = request.data.get('breadcrumb_id')
        
        if not breadcrumb_id:
            return Response(
                {'error': 'breadcrumb_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            breadcrumb = KnowledgeBaseItem.objects.get(id=breadcrumb_id)
            item.breadcrumbs.remove(breadcrumb)
            return Response({'status': 'Breadcrumb removed successfully'})
        except KnowledgeBaseItem.DoesNotExist:
            return Response(
                {'error': 'Breadcrumb item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def bulk_add_tags(self, request, pk=None):
        """
        Add multiple tags to this item.
        Body: {"tag_labels": ["tag1", "tag2", "tag3"]}
        """
        item = self.get_object()
        tag_labels = request.data.get('tag_labels', [])
        
        if not isinstance(tag_labels, list):
            return Response(
                {'error': 'tag_labels must be a list'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tags = []
        for label in tag_labels:
            tag, created = KnowledgeBaseItemTag.objects.get_or_create(label=label)
            tags.append(tag)
        
        item.tags.add(*tags)
        return Response({
            'status': f'Added {len(tags)} tags successfully',
            'tags': [tag.label for tag in tags]
        })

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Get items grouped by category with counts.
        """
        from django.db.models import Count
        
        categories = self.get_queryset().values('category').annotate(
            count=Count('id')
        ).order_by('category')
        
        result = {}
        for cat in categories:
            category_items = self.get_queryset().filter(category=cat['category'])
            result[cat['category']] = {
                'count': cat['count'],
                'items': self.get_serializer(category_items, many=True).data
            }
        
        return Response(result)