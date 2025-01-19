from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from apps.core.models import GameMasterImpactAction
from apps.game.services.action import special
from apps.game.services.action.accept import ActionAcceptor
from apps.game.services.action.factory import CharacterActionFactory, ManualCharacterActionPlayerServiceFactory, \
    GameMasterActionFactory
from apps.game.services.character.core import CharacterService
from ..serializers.openapi import CharacterActionSerializer, CharacterActionLogSerializer, \
    RegisterImpactActionSerializer, GameMasterCharacterActionSerializer, SpecialActionSerializer
from ...models import CharacterAction, Cycle, SpecialAction


class SpecialActionsViewSet(
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
        user = self.request.user
        qs = super().get_queryset()
        return qs


class CharacterActionsViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = CharacterAction.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=1),
    )
    serializer_class = CharacterActionSerializer
    permission_classes = [permissions.IsAuthenticated]

    action_factory = CharacterActionFactory()
    cycle_player_factory = ManualCharacterActionPlayerServiceFactory

    def get_queryset(self):
        user = self.request.user
        character = user.main_character
        qs = super().get_queryset()
        return qs.filter(initiator=character) | qs.filter(target=character)

    @transaction.atomic
    def perform_create(self, serializer):
        # add initiator to the data
        serializer.validated_data['initiator'] = self.request.user.main_character
        serializer.validated_data['cycle'] = Cycle.objects.current()
        super().perform_create(serializer)
        instance = serializer.instance
        acceptor = ActionAcceptor(
            action=instance,
            factory=self.action_factory,
        )
        acceptor.accept()
        if instance.immediate:
            svc = self.cycle_player_factory(cycle=Cycle.objects.current(), factory=self.action_factory)
            svc.apply_single_action(
                action=instance
            )

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser],
            serializer_class=serializers.Serializer)
    @transaction.atomic
    def next_cycle(self, request):
        svc = self.cycle_player_factory(cycle=Cycle.objects.current(), factory=self.action_factory)
        cycle = svc.play()
        return Response(data={'id': cycle.id})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def current_cycle(self, request):
        cycle = Cycle.objects.current()
        return Response(data={'id': cycle.id})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def scheduled_actions(self, request):
        actions = CharacterAction.objects.filter(
            cycle=Cycle.objects.current(),
        )
        serializer = CharacterActionSerializer(actions, many=True)
        return Response(data=serializer.data)


class GameMasterActionsViewSet(
    viewsets.ModelViewSet
):
    queryset = CharacterAction.objects.all()
    serializer_class = CharacterActionLogSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        SearchFilter,
    ]

    char_action_factory = CharacterActionFactory()
    action_acceptor_cls = ActionAcceptor

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser],
            serializer_class=RegisterImpactActionSerializer)
    @transaction.atomic
    def register_impact(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        factory = GameMasterActionFactory()
        act = factory.construct_player_action(GameMasterImpactAction(**serializer.validated_data))
        acceptor = self.action_acceptor_cls(
            action=act,
            factory=self.char_action_factory,
        )
        acceptor.accept()
        # TMP: Apply the impact immediately
        # svc.perform(act)
        return Response(data=serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser],
            serializer_class=GameMasterCharacterActionSerializer)
    @transaction.atomic
    def register_character_action(self, request):
        # add initiator to the data
        serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['cycle'] = Cycle.objects.current()
        super().perform_create(serializer)
        instance = serializer.instance
        acceptor = self.action_acceptor_cls(
            action=instance,
            factory=self.char_action_factory,
        )
        acceptor.accept()
        return Response(data=serializer.data)
