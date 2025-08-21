from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.models.skills import BaseSkill
from apps.game.services.skills.gm_factory import GmManualSkillCreationFactory
from apps.gamemaster.api.serializers.skill_factory import SkillCreateSerializer
from apps.school.models import School
from apps.skills.api.serializers.openapi import (
    LearnedSkillSerializer, LearnedSchoolSerializer, SkillSerializer
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


class SkillFactoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for game masters to create skills dynamically during gameplay.
    Provides skill factory functionality with comprehensive validation and documentation.
    """
    permission_classes = [permissions.IsAdminUser]
    skill_factory_service = GmManualSkillCreationFactory()
    serializer_class = SkillSerializer

    @extend_schema(
        summary="Create a new skill",
        description="This endpoint allows game masters to create a new skill using the skill factory service. "
                    "The skill will be created with the provided data and returned in the response.",
        request=SkillCreateSerializer,
        responses={
            status.HTTP_201_CREATED: SkillSerializer,
            status.HTTP_400_BAD_REQUEST: "Invalid data provided."
        }
    )
    @action(detail=False, methods=['post'])
    def new_skill(self, request):
        """
        Create a new skill using the skill factory service.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school_id = serializer.validated_data.get('school')
        if not school_id:
            gm_school = School.objects.filter(
                game_master_only=True
            ).first()
            if not gm_school:
                return Response(
                    {"detail": "No game master only school found."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.validated_data['school'] = gm_school.id

        serializer.validated_data.setdefault('effect', [])
        serializer.validated_data.setdefault('impact', [])
        serializer.validated_data.setdefault('cost', [])
        base_skill = BaseSkill(
            **serializer.validated_data
        )
        skill = self.skill_factory_service.create_skill(base_skill)
        return Response(
            self.get_serializer(skill).data,
            status=status.HTTP_201_CREATED
        )
