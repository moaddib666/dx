from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.character.api.filters.character import CharacterFilter, NPCFilter
from apps.character.api.serializers.openapi import OpenaiCharacterSerializer, CharacterInfoSerializer, \
    CharacterPathSerializer, \
    CharacterTemplateFullSerializer, CharacterGenericDataSerializer, CharacterStatsSerializer, \
    DetailStatSerializer, SwipeBaseStatSerializer
from apps.character.models import Character, Stat
from apps.core.models import CharacterGenericData
from apps.game.services.character import CharacterFactory
from apps.game.services.character.character_base_stats import CharacterBaseStatsService
from apps.game.services.character.core import CharacterService
from apps.game.services.character.template import CharacterTemplateService
from apps.game.services.rand_dice import DiceService


class ClientCharacterManagementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing characters in the client application.
    Provides read-only access to character data.

    1. **get_queryset**: Returns the queryset of characters for the authenticated user.
    2. **we se all active and non active characters**: Filters characters based on the user's main character's position and campaign.
    3. **no npc characters are allowed**: Ensures that only characters related to the user's main character's campaign are returned.
    4. **select character** allows client to choose a character to play with.
    """
    queryset = Character.objects.all()
    serializer_class = OpenaiCharacterSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CharacterFilter

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        # Filter characters owned by the user (both active and inactive)
        qs = qs.filter(
            owner=user,
            npc=False  # Exclude NPC characters
        )

        return qs

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    @transaction.atomic
    def select_character(self, request, pk=None):
        """
        Select a character as the user's main character.
        """
        user = request.user
        character = self.get_object()

        # Ensure the character belongs to the user
        if character.owner != user:
            return Response(
                {"detail": "You do not own this character."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Set as main character
        user.main_character = character
        user.save(update_fields=['main_character'])

        return Response({"detail": "Character selected successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def current_character(self, request):
        """
        Get the user's current main character.
        """
        user = request.user
        if not hasattr(user, 'main_character') or not user.main_character:
            return Response({"detail": "No main character selected."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user.main_character)
        return Response(data=serializer.data)


class OpenAISchoolsManagementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Character.objects.filter(is_active=True)
    serializer_class = OpenaiCharacterSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NPCFilter
    # TODO move TO THE GAME SETTINGS
    PLAYER_CREATION_LIMIT = 5

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if not user.is_superuser:
            qs = qs.filter(
                position=user.main_character.position,
                is_active=True
            )
        return qs.filter(
            campaign=user.main_character.campaign,
        )

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

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def character_details(self, request):
        user = request.user
        character = user.main_character
        if not character:
            return Response({"detail": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(character)
        return Response(data=serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated],
            serializer_class=CharacterInfoSerializer)
    def character_info(self, request):
        user = request.user
        try:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
        except Exception as e:
            pass
        try:
            character = user.main_character
            service = CharacterService(character)
            character_info = service.get_character_info()
            return Response(data=character_info.model_dump())
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
        user.main_character = char_svc.character
        user.save(update_fields=['main_character'])
        return Response(data=character_info.model_dump())

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated],
            serializer_class=CharacterStatsSerializer)
    def character_stats(self, request):
        user = request.user
        character = user.main_character
        serializer = self.get_serializer(character)
        return Response(data=serializer.data)


class OpenAICharacterGameMasterManagementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Character.objects.filter(is_active=True)
    serializer_class = OpenaiCharacterSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CharacterFilter

    @action(detail=True, methods=['get'],
            serializer_class=CharacterInfoSerializer)
    def character_info(self, request, pk=None):

        try:
            character = self.get_object()
            service = CharacterService(character)
            character_info = service.get_character_info()
            return Response(data=character_info.model_dump())
        except Character.DoesNotExist:
            return Response({"detail": "Character not found."}, status=status.HTTP_404_NOT_FOUND)


class OpenAICharacterManageBaseStats(viewsets.ReadOnlyModelViewSet):
    queryset = Stat.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    serializer_class = DetailStatSerializer

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(
            character=user.main_character,
        )

    @extend_schema(
        request=None,  # No request body expected
        responses=DetailStatSerializer(many=True),
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    @transaction.atomic
    def reset_base_stats(self, request):
        user = request.user
        character = user.main_character
        if not character.resetting_base_stats:
            return Response({"detail": "Character is not resetting base stats."}, status=status.HTTP_400_BAD_REQUEST)
        service = CharacterBaseStatsService(character, DiceService)
        instance = service.reset_base_stats()
        serializer = self.get_serializer(instance, many=True)
        return Response(data=serializer.data)

    @extend_schema(
        request=SwipeBaseStatSerializer,
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    @transaction.atomic
    def swipe_base_stat(self, request, pk=None):
        user = request.user
        character = user.main_character
        if not character.resetting_base_stats:
            return Response({"detail": "Character is not resetting base stats."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SwipeBaseStatSerializer(data=request.data, context={})
        serializer.is_valid(raise_exception=True)
        service = CharacterBaseStatsService(character, DiceService)
        stat_from = get_object_or_404(Stat, pk=serializer.validated_data['from_stat'])
        stat_to = get_object_or_404(Stat, pk=serializer.validated_data['to_stat'])
        service.switch_base_stats(
            stat_1=stat_from,
            stat_2=stat_to
        )
        response_serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=response_serializer.data)
