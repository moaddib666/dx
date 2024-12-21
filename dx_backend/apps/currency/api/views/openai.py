from rest_framework import viewsets, permissions

from apps.currency.api.serializers.openapi import PlayerCurrencySerializer, CurrencyTokenSerializer
from apps.currency.models import PlayerCurrency, CurrencyToken


class OpenAIWorldCurrencyTokensViewSet(
    viewsets.ModelViewSet):
    queryset = CurrencyToken.objects.all()

    serializer_class = CurrencyTokenSerializer
    permission_classes = [permissions.IsAdminUser]


class OpenAIPlayerCurrencyTokensViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = PlayerCurrency.objects.filter()
    serializer_class = PlayerCurrencySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(player=user.player)
