import logging
from typing import TYPE_CHECKING, Self

from apps.game.exceptions import GameLogicException
from apps.game.services.player.core import PlayerService

if TYPE_CHECKING:
    from apps.fight.models import DuelInvitation


class InvitationService:
    logger = logging.getLogger("game.services.invitation.InvitationService")

    def __init__(self, invitation):
        self.invitation = invitation
        self.player1 = PlayerService(invitation.initiator)
        self.player2 = PlayerService(invitation.targets)

    @classmethod
    def create(cls, player1: PlayerService, player2: PlayerService) -> "Self":
        cls.logger.debug(f"Creating duel invitation between {player1.player.name} and {player2.player.name}")
        if player1.player.id == player2.player.id:
            raise GameLogicException("Fuck")
        if player1.player.current_location != player2.player.current_location:
            raise GameLogicException('Players are not in the same location')
        if player1.player.fight_id or player2.player.fight_id:
            raise GameLogicException('One of the players is already in a fight')
        invitation = player1.player.duel_invitations_sent.create(target=player2.player)
        cls.logger.info(f"Duel invitation was successfully created from {player1.player.name} to {player2.player.name}")
        service = cls(invitation)
        return service

    def invite(self) -> "DuelInvitation":
        self.notify_players()
        return self.invitation

    def notify_players(self):
        self.player1.notify(self._create_event(self.invitation))
        self.player2.notify(self._create_event(self.invitation))

    def accept(self) -> "DuelInvitation":
        if self.invitation.is_accepted:
            raise GameLogicException('Invitation is already accepted')
        if self.invitation.is_rejected:
            raise GameLogicException('Invitation is already rejected')
        if self.player1.player.fight_id or self.player2.player.fight_id:
            raise GameLogicException('One of the players is already in a fight')
        self.invitation.is_accepted = True
        self.invitation.save()
        return self.invitation

    def _serialize_invitation(self, invitation):
        return {
            'id': invitation.id,
            'initiator': {
                'id': invitation.initiator.id,
                'name': invitation.initiator.name,
            },
            'target': {
                'id': invitation.targets.id,
                'name': invitation.targets.name,
            },
            'is_accepted': invitation.is_accepted,
            'is_rejected': invitation.is_rejected,
            'fight': invitation.fight_id,
        }

    def _create_event(self, invitation):
        # TODO: implement message bus
        return {
            'type': 'duel_invitation',
            'data': self._serialize_invitation(invitation),
        }

    def reject(self):
        if self.invitation.is_accepted:
            raise GameLogicException('Invitation is already accepted')
        self.invitation.is_rejected = True
        self.invitation.save()
        self.notify_players()
