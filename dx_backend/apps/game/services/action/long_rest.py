from apps.action.models import CharacterAction
from apps.game.exceptions import GameException
from apps.game.services.action.base_service import CharacterActionServicePrototype
from apps.game.services.character.core import CharacterService


class CharacterLongRestService(CharacterActionServicePrototype):
    character_svc_cls = CharacterService

    def perform(self, action: CharacterAction):
        char_svc = self.character_svc_cls(action.initiator)
        char_svc.refill_all()

    def check(self, action: CharacterAction):
        char_svc = self.character_svc_cls(action.initiator)
        if not char_svc.is_in_safe_place():
            raise GameException("Character is not in a safe place")

    def check_acceptance(self, action: CharacterAction):
        # Character must have action points to move at least 1 point
        char_svc = self.character_svc_cls(action.initiator)
        if char_svc.get_current_ap() < 1:
            raise GameException("Not enough action points")
        if char_svc.get_current_hp() < 1:
            raise GameException("Character is dead")

        # character must be in a safe place to rest
        if not char_svc.is_in_safe_place():
            raise GameException("Character is not in a safe place")

    def accept(self, action: CharacterAction):
        char_svc = self.character_svc_cls(action.initiator)
        char_svc.spend_all_ap()
