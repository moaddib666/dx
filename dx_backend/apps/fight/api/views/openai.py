from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.fight.api.serializers.openapi import DuelInvitationSerializer, FightSerializer, FightTurnActionSerializer, \
    CurrentFightSerializer
from apps.fight.models import DuelInvitation, Fight, FightTurnAction
from apps.game.exceptions import GameLogicException
from apps.game.helpers import get_brief_info
from apps.game.services.action.factory import FightActionFactory
from apps.game.services.fight.duel import InvitationService
from apps.game.services.fight.fight import FightService
from apps.game.services.player.core import PlayerService


class DuelInvitationViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = DuelInvitation.objects.filter(
        is_accepted=False,
        is_rejected=False,
        fight__isnull=True,
        created_at__gte=timezone.now() - timedelta(minutes=5),
    )
    serializer_class = DuelInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    PLAYER_CREATION_LIMIT = 5

    def get_queryset(self):
        user = self.request.user
        player = user.player
        qs = super().get_queryset()
        return qs.filter(target=player)

    @transaction.atomic
    def perform_create(self, serializer):
        player1_service = PlayerService(self.request.user.player)
        player2_service = PlayerService(serializer.validated_data['target'])
        InvitationService.create(player1_service, player2_service).invite()

    @action(detail=True, methods=['post'], serializer_class=None)
    @transaction.atomic
    def accept(self, request, pk=None):
        invitation = self.get_object()
        service = InvitationService(invitation)
        invitation = service.accept()
        fight_svc = FightService.create_from_duel_invitation(service)
        invitation.fight = fight_svc.fight
        invitation.save()
        service.notify_players()
        return Response(status=status.HTTP_200_OK, data=DuelInvitationSerializer(invitation).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        invitation = self.get_object()
        InvitationService(invitation).reject()
        return Response(status=status.HTTP_200_OK, data=DuelInvitationSerializer(invitation).data)


class FightViewSet(
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FightSerializer
    queryset = Fight.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        player = user.player
        qs = super().get_queryset()
        return qs.filter(side_a_participants=player) | qs.filter(side_b_participants=player)

    # TODO: implement fight list in current location
    # TODO: implement duel list in current location
    # TODO: implement fight details (for current location)

    def get_current_fight(self) -> Fight:
        user = self.request.user
        player = user.player
        fight = player.fight
        if not fight:
            raise GameLogicException("Not in the fight.")
        return fight

    @action(detail=False, methods=['get'], serializer_class=CurrentFightSerializer)
    def current(self, request):
        fight = self.get_current_fight()

        side_a = fight.side_a_participants.all()
        side_b = fight.side_b_participants.all()
        if request.user.player in side_a:
            allies = side_a
            enemies = side_b
        else:
            allies = side_b
            enemies = side_a
        # TODO: get info from service
        serializer = self.get_serializer(
            {
                'fight': fight,
                'allies': [get_brief_info(a) for a in allies.exclude(id=request.user.player.id)],
                'enemies': [get_brief_info(e) for e in enemies],
            }
        )
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def history(self, request):
        fights = self.get_queryset().filter(is_open=False).order_by('-created_at')
        serializer = self.get_serializer(fights, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        fight = self.get_current_fight()
        player_service = PlayerService(self.request.user.player)
        FightService(fight).leave(player_service)
        return Response(status=status.HTTP_200_OK, data=FightSerializer(fight).data)

    @action(detail=True, methods=['post'])
    def join_to_attacker_side(self, request, pk=None):
        fight = self.get_object()
        player_service = PlayerService(self.request.user.player)
        FightService(fight).join(player_service, side='a')
        return Response(status=status.HTTP_200_OK, data=FightSerializer(fight).data)

    @action(detail=True, methods=['post'])
    def join_to_defender_side(self, request, pk=None):
        fight = self.get_object()
        player_service = PlayerService(self.request.user.player)
        FightService(fight).join(player_service, side='b')
        return Response(status=status.HTTP_200_OK, data=FightSerializer(fight).data)


class FightActionsViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = FightTurnAction.objects.filter()
    serializer_class = FightTurnActionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        player = user.player
        fight = player.fight
        qs = super().get_queryset()
        return qs.filter(tyrn__fight=fight)

    @transaction.atomic
    def perform_create(self, serializer):
        if not self.request.user.player.fight:
            raise GameLogicException("Not in the fight.")
        if not self.request.user.player.fight.current_turn:
            raise GameLogicException("Fight is not started.")

        fight_action = serializer.save(initiator=self.request.user.player,
                                       turn=self.request.user.player.fight.current_turn)

        action_svc = FightActionFactory().from_action(fight_action)
        action_svc.check()

        return super().perform_create(serializer)
