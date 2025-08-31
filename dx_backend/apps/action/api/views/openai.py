from datetime import timedelta

from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from apps.core.models import GameMasterImpactAction, CharacterActionType
from apps.core.utils.api import CampaignFilterMixin
from apps.game.services.action import special
from apps.game.services.action.factory import GameMasterActionFactory
from apps.game.services.character.core import CharacterService
from apps.gamemaster.tools import ACTION_PIPELINE_TOOL
from ..serializers.cycle import GameCycleSerializer
from ..serializers.openapi import CharacterActionSerializer, GameMasterCharacterActionLogSerializer, \
    RegisterImpactActionSerializer, GameMasterCharacterActionSerializer, SpecialActionSerializer, \
    CharacterActionLogSerializer, DiceRollResultSerializer
from ...models import CharacterAction, Cycle, SpecialAction


class SpecialActionsViewSet(
    CampaignFilterMixin,
    viewsets.ReadOnlyModelViewSet
):
    queryset = SpecialAction.objects.all()
    serializer_class = SpecialActionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def available(self, request):
        user = request.user
        character = user.main_character
        acceptable = []
        factory = special.AcceptanceFactory()
        for act in self.queryset:
            rule = factory.from_action(act)
            if rule.is_acceptable(CharacterService(character)):
                acceptable.append(act)
        serializer = self.get_serializer(acceptable, many=True, context=self.get_serializer_context())
        return Response(data=serializer.data)


class CharacterActionsLogViewSet(
    CampaignFilterMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = CharacterAction.objects.all()
    serializer_class = CharacterActionLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        SearchFilter,
    ]

    # all actions for now
    def get_queryset(self):
        """
        Return actions for:
         1. the current user main character
         2. the current user main character as a target
         3. the current user main character position
        """
        user = self.request.user
        main_character = user.main_character
        # Get the campaign from the main character
        campaign = self.request.user.current_campaign
        cycles = Cycle.objects.filter(campaign=campaign).order_by('-number')[:3]
        current_cycle = Cycle.objects.current(campaign=campaign)
        # FIXME:
        #  - show all actions for last 3 cycles
        #  - Filter our actions form the current cycle that was not initiated by the main character
        last2cycles = super().get_queryset().filter(
            cycle__campaign=campaign,
            accepted=True,
            cycle__in=cycles[:2],
            position=main_character.position,
        )
        current_cycle_qs = super().get_queryset().filter(
            cycle=current_cycle,
            accepted=True,
        ).filter(
            initiator=main_character
        )
        qs = (last2cycles | current_cycle_qs).distinct().order_by('-cycle', 'accepted', 'order')
        return qs



class CharacterActionsViewSet(
    CampaignFilterMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = CharacterAction.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=1),
    )
    serializer_class = CharacterActionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        campaign = self.request.user.current_campaign
        character = user.main_character
        qs = super().get_queryset().filter(
            cycle__campaign=campaign,
            cycle__isnull=False,
        )
        return qs.filter(initiator=character) | qs.filter(target=character)

    @transaction.atomic
    def perform_create(self, serializer):
        # add initiator to the data
        initiator = self.request.user.main_character
        serializer.validated_data['initiator'] = initiator
        # Get the campaign from the initiator
        campaign = initiator.campaign if initiator else None
        serializer.validated_data['cycle'] = Cycle.objects.current(campaign=campaign)
        serializer.validated_data['position'] = serializer.validated_data['initiator'].position
        super().perform_create(serializer)
        instance = serializer.instance

        # Use the action pipeline to process the action
        ACTION_PIPELINE_TOOL.chain(instance).execute()

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser],
            serializer_class=serializers.Serializer)
    def next_cycle(self, request):
        # Get the campaign from the user's main character
        campaign = self.request.user.current_campaign

        current_cycle = Cycle.objects.current(campaign=campaign)
        svc = ACTION_PIPELINE_TOOL.cycle_player_factory(
            cycle=current_cycle,
            factory=ACTION_PIPELINE_TOOL.action_factory
        )
        cycle = svc.play()
        return Response(data={'id': cycle.id})

    @extend_schema(
        responses={
            200: GameCycleSerializer(),
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def current_cycle(self, request):
        # Get the campaign from the user's main character
        campaign = None
        if request.user.is_authenticated and hasattr(request.user, 'main_character') and request.user.main_character:
            campaign = request.user.main_character.campaign
        cycle = Cycle.objects.current(campaign=campaign)
        return Response(data=GameCycleSerializer(cycle).data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def scheduled_actions(self, request):
        # Get the campaign from the user's main character
        campaign = None
        if request.user.is_authenticated and hasattr(request.user, 'main_character') and request.user.main_character:
            campaign = request.user.main_character.campaign

        actions = CharacterAction.objects.filter(
            cycle=Cycle.objects.current(campaign=campaign),
        )
        serializer = CharacterActionSerializer(actions, many=True)
        return Response(data=serializer.data)

    @extend_schema(
        responses={
            200: DiceRollResultSerializer,
        }
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated],
            serializer_class=serializers.Serializer)
    def roll_d20_dice(self, request):
        """
        Roll dice endpoint that creates a dice roll action, executes it immediately,
        and returns the dice outcome result.
        """
        sides = 20

        # Get the user's main character
        initiator = request.user.main_character
        if not initiator:
            return Response(
                {'error': 'No main character found for user'},
                status=400
            )

        # Get the campaign from the initiator
        campaign = initiator.campaign
        if not campaign:
            return Response(
                {'error': 'Character is not in a campaign'},
                status=400
            )

        # Create dice roll action
        action = CharacterAction.objects.create(
            action_type=CharacterActionType.DICE_ROLL,
            initiator=initiator,
            data={'sides': sides},
            position=initiator.position,
            cycle=Cycle.objects.current(campaign=campaign),
            immediate=True,
            challenge=initiator.challenge,
        )

        # Execute the action immediately using the action pipeline
        ACTION_PIPELINE_TOOL.chain(action).execute()

        # Get the dice roll result from the action's impacts
        dice_result = None
        for impact in action.impacts.all():
            if impact.dice_roll_result:
                dice_result = impact.dice_roll_result
                break

        if not dice_result:
            return Response(
                {'error': 'Failed to get dice roll result'},
                status=500
            )

        # Serialize and return the dice roll result
        serializer = DiceRollResultSerializer(dice_result)
        return Response(serializer.data)


class GameMasterActionsViewSet(
    CampaignFilterMixin,
    viewsets.ModelViewSet
):
    queryset = CharacterAction.objects.all()
    serializer_class = GameMasterCharacterActionLogSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        SearchFilter,
    ]

    def get_queryset(self):
        campaign = self.request.user.current_campaign
        return super().get_queryset().filter(
            cycle__campaign=campaign,
            cycle__isnull=False,
        )

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser],
            serializer_class=RegisterImpactActionSerializer)
    @transaction.atomic
    def register_impact(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        factory = GameMasterActionFactory()
        act = factory.construct_player_action(GameMasterImpactAction(**serializer.validated_data))

        # Use the action pipeline to process the action
        ACTION_PIPELINE_TOOL.chain(act).execute()

        return Response(data=serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser],
            serializer_class=GameMasterCharacterActionSerializer)
    @transaction.atomic
    def register_character_action(self, request):
        # add initiator to the data
        serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        # Get the campaign from the user's main character
        campaign = None
        if request.user.is_authenticated and hasattr(request.user, 'main_character') and request.user.main_character:
            campaign = request.user.main_character.campaign

        serializer.validated_data['cycle'] = Cycle.objects.current(campaign=campaign)
        super().perform_create(serializer)
        instance = serializer.instance

        # Use the action pipeline to process the action
        ACTION_PIPELINE_TOOL.chain(instance).execute()

        return Response(data=serializer.data)
