from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.modificators.api.serializers.openapi import ModificatorSerializer, CharacterModificatorSerializer
from apps.modificators.models import Modificator, CharacterModificator


class OpenAIWorldModificatorsViewSet(
    viewsets.ModelViewSet):
    queryset = Modificator.objects.all()

    serializer_class = ModificatorSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny], authentication_classes=[])
    def get_all_modificators(self, request):
        modificators = self.get_queryset()
        serializer = ModificatorSerializer(modificators, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class OpenAICharacterModificatorsViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = CharacterModificator.objects.filter()
    serializer_class = CharacterModificatorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(character=user.character)
