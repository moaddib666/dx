from rest_framework import viewsets, permissions

from apps.fight.api.serializers.openapi import FightGenericSerializer
from apps.fight.models import Fight


class FightViewSet(
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FightGenericSerializer
    queryset = Fight.objects.all()
    permission_classes = [permissions.IsAuthenticated]
