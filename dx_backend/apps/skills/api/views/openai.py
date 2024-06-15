from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.game.services.player.player_schools import PlayerSchoolService
from apps.game.services.player.player_skills import PlayerSkillsService
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
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(player=user.player)

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        skill = serializer.validated_data['skill']
        PlayerSkillsService().add(user.player, skill)
        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    def perform_destroy(self, instance):
        PlayerSkillsService().remove(self.request.user.player, instance)
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
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(player=user.player)

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        school = serializer.validated_data['school']
        PlayerSchoolService().add(user.player, school)
        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    def perform_destroy(self, instance):
        PlayerSchoolService().remove(self.request.user.player, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)