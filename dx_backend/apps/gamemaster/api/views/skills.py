from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.skills.api.serializers.openapi import (
    LearnedSkillSerializer, LearnedSchoolSerializer
)
from apps.skills.models import LearnedSkill, LearnedSchool


class GameMasterLearnedSkillViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage learned skills.
    This viewset provides full CRUD operations for learned skills.
    """
    queryset = LearnedSkill.objects.all()
    serializer_class = LearnedSkillSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class GameMasterLearnedSchoolViewSet(viewsets.ModelViewSet):
    """
    ViewSet for game masters to manage learned schools.
    This viewset provides full CRUD operations for learned schools.
    """
    queryset = LearnedSchool.objects.all()
    serializer_class = LearnedSchoolSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]