from rest_framework import viewsets, permissions
from rest_framework.response import Response

from apps.core.api.serializers.openapi import CharacterStatSerializer, StatObjectSerializer, ViolationObjectSerializer
from apps.core.models import CharacterStats, StatObject, ViolationObject
from apps.core.services import CharacterStatPresenter


class CharacterStatsViewSet(
    viewsets.ViewSet):
    serializer_class = CharacterStatSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def list(self, request):
        presentor = CharacterStatPresenter(CharacterStats)
        return Response(data=presentor.prest_as_list(), status=200)


class StatViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatObjectSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    queryset = StatObject.objects.all()


class ViolationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ViolationObjectSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    queryset = ViolationObject.objects.all()
