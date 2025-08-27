from rest_framework import viewsets, permissions

from apps.dice.api.serializers.challenge import ChallengeGenericSerializer
from apps.dice.models import Challenge


class ChallengeViewSet(
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ChallengeGenericSerializer
    queryset = Challenge.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter queryset to only include challenges for the authenticated user main character.
        """
        user = self.request.user
        if not user.is_authenticated:
            return Challenge.objects.none()

        character = getattr(user, 'main_character', None)
        if character is None:
            return Challenge.objects.none()

        return self.queryset.filter(target=character).prefetch_related("modifiers", "outcome")
