from rest_framework import viewsets, permissions

from apps.items.api.serializers.openapi import PlayerItemSerializer, ItemSerializer
from apps.items.models import PlayerItem, Item


class OpenAIPlayerItemsViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = PlayerItem.objects.filter()
    serializer_class = PlayerItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(player=user.player)


class WorldItemsViewSet(
    viewsets.ModelViewSet
):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAdminUser]
