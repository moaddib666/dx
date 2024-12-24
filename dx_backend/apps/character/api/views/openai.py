from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.character.api.serializers.openapi import OpenaiCharacterSerializer, CharacterInfoSerializer, \
    CharacterPathSerializer, \
    CharacterTemplateFullSerializer, CharacterGenericDataSerializer
from apps.character.models import Character
from apps.core.models import CharacterGenericData
from apps.game.services.character import CharacterFactory
from apps.game.services.character.core import CharacterService
from apps.game.services.character.template import CharacterTemplateService


class OpenAISchoolsManagementViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.filter(is_active=True)
    serializer_class = OpenaiCharacterSerializer
    permission_classes = [permissions.IsAdminUser]

    # TODO move TO THE GAME SETTINGS
    PLAYER_CREATION_LIMIT = 5

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser:
            return qs
        return Character.objects.filter(owner=user)

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user

        # Check the limit
        current_character_count = Character.objects.filter(owner=user).count()
        if current_character_count >= self.PLAYER_CREATION_LIMIT:
            return Response(
                {'detail': f'Character creation limit of {self.PLAYER_CREATION_LIMIT} reached.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        factory = CharacterFactory(user)
        character = factory.create_character(
            name=serializer.validated_data['name'],
            age=serializer.validated_data['age'],
            gender=serializer.validated_data['gender'],
        )
        serializer.instance = character

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated],
            serializer_class=CharacterInfoSerializer)
    def character_info(self, request):
        user = request.user
        try:
            character = user.main_character
            service = CharacterService(character)
            character_info = service.get_character_info()
            return Response(data=character_info.dict())
        except Character.DoesNotExist:
            return Response({"detail": "Character not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated],
            serializer_class=CharacterPathSerializer)
    def chose_path(self, request, pk=None):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            character = user.main_character
            service = CharacterService(character)
            service.chose_path(serializer.validated_data['path'])
            return Response({"detail": "Path chosen."})
        except Character.DoesNotExist:
            return Response({"detail": "Character not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny], authentication_classes=[],
            serializer_class=CharacterTemplateFullSerializer, )
    def character_template(self, request):
        svc = CharacterTemplateService(9)
        template = svc.create_template()
        return Response(data=template.model_dump())

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated],
            serializer_class=CharacterGenericDataSerializer)
    @transaction.atomic
    def import_character(self, request):
        """
        Create a new character for the user.

        """
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        svc = CharacterFactory(user)
        char_svc = svc.import_character(CharacterGenericData(**serializer.validated_data))
        character_info = char_svc.get_character_info()
        return Response(data=character_info.model_dump())
