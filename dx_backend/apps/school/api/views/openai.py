from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def get_all_paths(self, request):
        paths = ThePath.objects.all()
        serializer = OpenaiPathSerializer(paths, many=True)
        return Response(serializer.data)


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

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def get_all_schools(self, request, path_pk=None):
        schools = School.objects.all()
        serializer = OpenaiSchoolSerializer(schools, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def get_all_skills(self, request, school_pk=None):
        skills = Skill.objects.all()
        serializer = OpenaiSkillSerializer(skills, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser], serializer_class=OpenaiSkillSerializer)
    def create_skill(self, request, *args, **kwargs):
        school = self.get_object()
        serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['school'] = school
        serializer.save()
        return Response(data=serializer.data, status=201)


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

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def get_all_school_skills(self, request, school_pk=None):
        skills = Skill.objects.all()
        serializer = OpenaiSkillSerializer(skills, many=True)
        return Response(serializer.data)
