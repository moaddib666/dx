from rest_framework import viewsets, permissions

from apps.modificators.api.serializers.openapi import ModificatorSerializer, PlayerModificatorSerializer
from apps.modificators.models import Modificator, PlayerModificator


class OpenAIWorldModificatorsViewSet(
    viewsets.ModelViewSet):
    queryset = Modificator.objects.all()

    serializer_class = ModificatorSerializer
    permission_classes = [permissions.IsAdminUser]


class OpenAIPlayerModificatorsViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = PlayerModificator.objects.filter()
    serializer_class = PlayerModificatorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(player=user.player)
