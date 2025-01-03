from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from apps.shields.api.serializers.openapi import ActiveShieldSerializer
from apps.shields.filters import CharacterActiveShieldFilter
from apps.shields.models import ActiveShield


class OpenAIActiveShieldsViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = ActiveShield.objects.filter()
    serializer_class = ActiveShieldSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(target=user.main_character)


class GameMasterOpenAIActiveShieldsViewSet(viewsets.mixins.ListModelMixin,
                                           viewsets.GenericViewSet):
    queryset = ActiveShield.objects.all()
    serializer_class = ActiveShieldSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CharacterActiveShieldFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(target__is_active=True)
