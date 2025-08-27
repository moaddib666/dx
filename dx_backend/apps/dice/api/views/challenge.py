from rest_framework import viewsets, permissions

from apps.dice.api.serializers.challenge import ChallengeGenericSerializer
from apps.dice.models import Challenge


class ChallengeViewSet(
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ChallengeGenericSerializer
    queryset = Challenge.objects.all()
    permission_classes = [permissions.IsAuthenticated]
