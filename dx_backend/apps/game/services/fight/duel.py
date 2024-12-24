import logging
from typing import TYPE_CHECKING, Self

from apps.core.bus.base import GameEvent
from apps.game.exceptions import GameLogicException
from apps.game.services.character.core import CharacterService

if TYPE_CHECKING:
    from apps.fight.models import DuelInvitation


class InvitationService:
    logger = logging.getLogger("game.services.invitation.InvitationService")

    def __init__(self, invitation):
        self.invitation = invitation
        self.character1 = CharacterService(invitation.initiator)
        self.character2 = CharacterService(invitation.targets)

    @classmethod
    def create(cls, character1: CharacterService, character2: CharacterService) -> "Self":
        cls.logger.debug(f"Creating duel invitation between {character1.character.name} and {character2.character.name}")
        if character1.character.id == character2.character.id:
            raise GameLogicException("Fuck")
        if character1.character.current_location != character2.character.current_location:
            raise GameLogicException('Characters are not in the same location')
        if character1.character.fight_id or character2.character.fight_id:
            raise GameLogicException('One of the characters is already in a fight')
        invitation = character1.character.duel_invitations_sent.create(target=character2.character)
        cls.logger.info(f"Duel invitation was successfully created from {character1.character.name} to {character2.character.name}")
        service = cls(invitation)
        return service

    def invite(self) -> "DuelInvitation":
        self.notify_characters()
        return self.invitation

    def notify_characters(self):
        self.character1.notify(self._create_event(self.invitation))
        self.character2.notify(self._create_event(self.invitation))

    def accept(self) -> "DuelInvitation":
        if self.invitation.is_accepted:
            raise GameLogicException('Invitation is already accepted')
        if self.invitation.is_rejected:
            raise GameLogicException('Invitation is already rejected')
        if self.character1.character.fight_id or self.character2.character.fight_id:
            raise GameLogicException('One of the characters is already in a fight')
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

    def _create_event(self, invitation) -> GameEvent:
        # TODO: implement message bus
        return GameEvent.create(
            name="invitation",
            category="duel",
            data=self._serialize_invitation(invitation),
        )

    def reject(self):
        if self.invitation.is_accepted:
            raise GameLogicException('Invitation is already accepted')
        self.invitation.is_rejected = True
        self.invitation.save()
        self.notify_characters()
