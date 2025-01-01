from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status, pagination
from rest_framework.response import Response

from apps.game.services.character.character_schools import CharacterSchoolService
from apps.game.services.character.character_skills import CharacterSkillsService
from apps.skills.api.filters import CharacterLearnedSkillFilter
from apps.skills.api.serializers.openapi import LearnedSkillSerializer, LearnedSchoolSerializer
from apps.skills.models import LearnedSkill, LearnedSchool


class OpenAILearnedSkillsViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = LearnedSkill.objects.filter()
    serializer_class = LearnedSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(character=user.main_character)

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        skill = serializer.validated_data['skill']
        CharacterSkillsService().add(user.main_character, skill)
        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    def perform_destroy(self, instance):
        CharacterSkillsService().remove(self.request.user.main_character, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OpenAILearnedSchoolsViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = LearnedSchool.objects.filter()
    serializer_class = LearnedSchoolSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(character=user.main_character)

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        school = serializer.validated_data['school']
        CharacterSchoolService().add(user.main_character, school)
        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    def perform_destroy(self, instance):
        CharacterSchoolService().remove(self.request.user.main_character, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GameMasterOpenAILearnedSkillsViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    class StandardResultsSetPagination(pagination.PageNumberPagination):
        page_size = 100
        page_size_query_param = 'page_size'
        max_page_size = 200

    queryset = LearnedSkill.objects.filter()
    serializer_class = LearnedSkillSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CharacterLearnedSkillFilter

