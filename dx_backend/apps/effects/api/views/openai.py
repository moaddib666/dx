from rest_framework import viewsets, permissions

from apps.effects.api.serializers.openapi import ActiveEffectSerializer
from apps.effects.models import ActiveEffect


class OpenAIActiveEffectsViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = ActiveEffect.objects.filter()
    serializer_class = ActiveEffectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(target=user.main_character)
