from rest_framework import viewsets, permissions
from rest_framework.response import Response

from apps.core.api.serializers.openapi import CharacterStatSerializer
from apps.core.models import CharacterStats
from apps.core.services import CharacterStatPresenter


class CharacterStatsViewSet(
    viewsets.ViewSet):
    serializer_class = CharacterStatSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def list(self, request):
        presentor = CharacterStatPresenter(CharacterStats)
        return Response(data=presentor.prest_as_list(), status=200)
