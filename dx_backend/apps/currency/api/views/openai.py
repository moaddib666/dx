from rest_framework import viewsets, permissions

from apps.currency.api.serializers.openapi import CharacterCurrencySerializer, CurrencyTokenSerializer
from apps.currency.models import CharacterCurrency, CurrencyToken


class OpenAIWorldCurrencyTokensViewSet(
    viewsets.ModelViewSet):
    queryset = CurrencyToken.objects.all()

    serializer_class = CurrencyTokenSerializer
    permission_classes = [permissions.IsAdminUser]


class OpenAICharacterCurrencyTokensViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = CharacterCurrency.objects.filter()
    serializer_class = CharacterCurrencySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(character=user.character)
