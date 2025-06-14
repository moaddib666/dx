from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.school.api.serializers.openapi import (
    OpenaiSchoolSerializer, OpenaiSkillSerializer, OpenaiPathSerializer, OpenaiPathWithSchoolsSerializer
)
from apps.school.models import School, Skill, ThePath


class GameMasterSchoolViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage schools.
    This viewset provides full CRUD operations for schools.
    """
    queryset = School.objects.all()
    serializer_class = OpenaiSchoolSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterSkillViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage skills.
    This viewset provides full CRUD operations for skills.
    """
    queryset = Skill.objects.all()
    serializer_class = OpenaiSkillSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterPathViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage paths.
    This viewset provides full CRUD operations for paths.
    """
    queryset = ThePath.objects.all()
    serializer_class = OpenaiPathSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]

    @action(detail=True, methods=['get'], serializer_class=OpenaiPathWithSchoolsSerializer)
    def with_schools(self, request, pk=None):
        """
        Get a path with its schools.
        """
        path = self.get_object()
        serializer = self.get_serializer(path)
        return Response(serializer.data)