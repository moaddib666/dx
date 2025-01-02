from rest_framework import viewsets, permissions

from apps.items.api.serializers.openapi import CharacterItemSerializer, ItemSerializer
from apps.items.models import CharacterItem, Item


class OpenAICharacterItemsViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = CharacterItem.objects.filter()
    serializer_class = CharacterItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(character=user.main_character)


class WorldItemsViewSet(
    viewsets.ModelViewSet
):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAdminUser]
