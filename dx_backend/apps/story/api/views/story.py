from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.story.models import Story, Chapter, Quest, Condition, Reward
from apps.core.models import Trigger
from apps.story.api.serializers import (
    StorySerializer,
    StoryDetailSerializer,
    ChapterSerializer,
    QuestSerializer,
    ConditionSerializer,
    RewardSerializer,
    TriggerSerializer
)


class StoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage stories.
    
    This viewset provides operations for:
    - Listing, retrieving, creating, updating, and deleting stories
    - Managing story canonical status
    - Filtering stories by tags and canonical status
    """
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['canonical']
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['title', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action == 'retrieve':
            return StoryDetailSerializer
        return StorySerializer

    @action(detail=True, methods=['post'])
    def set_canonical(self, request, pk=None):
        """
        Set a story as canonical (requires owner review).
        """
        story = self.get_object()
        story.canonical = True
        story.save()
        return Response({'status': 'Story set as canonical'})

    @action(detail=True, methods=['post'])
    def unset_canonical(self, request, pk=None):
        """
        Remove canonical status from a story.
        """
        story = self.get_object()
        story.canonical = False
        story.save()
        return Response({'status': 'Canonical status removed'})


class ChapterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage chapters within stories.
    """
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['story']
    ordering_fields = ['order', 'title', 'created_at']
    ordering = ['order']


class QuestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage quests within chapters.
    """
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['chapter', 'chapter__story']
    ordering_fields = ['order', 'title', 'cycle_limit', 'created_at']
    ordering = ['order']


class ConditionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage conditions for quest starters and objectives.
    """
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']


class RewardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage rewards for quest success/failure.
    """
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['experience', 'created_at']
    ordering = ['-experience']


class TriggerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage triggers for quest conditions.
    """
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type', 'game_object', 'position', 'location']
    search_fields = ['description']
