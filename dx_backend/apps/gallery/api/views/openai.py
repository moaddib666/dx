from rest_framework import viewsets, permissions

from apps.gallery.api.serializers.openapi import ArtSerializer
from apps.gallery.models import Art


class WorldGalleryViewSet(
    viewsets.ReadOnlyModelViewSet
):
    queryset = Art.objects.all()
    serializer_class = ArtSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
