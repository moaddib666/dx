from rest_framework import viewsets, permissions
from apps.school.api.serializers.openapi import OpenaiSchoolSerializer, OpenaiSkillSerializer, OpenaiPathSerializer
from apps.school.models import School, Skill, ThePath


class OpenAIPathManagementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ThePath.objects.all()
    serializer_class = OpenaiPathSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs
        return qs.filter(school__path=user.player.path)


class OpenAISchoolManagementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OpenaiSchoolSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = School.objects.all()
        if user.is_superuser:
            return qs
        return qs.filter(path=user.player.path)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['path_id'] = self.kwargs.get('path_pk')
        return context


class OpenAISkillManagementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OpenaiSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        school_id = self.kwargs.get('school_pk')
        qs = Skill.objects.filter(school__id=school_id)
        if user.is_superuser:
            return qs
        return qs.filter(school__path=user.player.path, grade__lte=user.player.grade)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['school_id'] = self.kwargs.get('school_pk')
        return context

