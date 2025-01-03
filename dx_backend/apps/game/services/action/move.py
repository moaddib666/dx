from apps.action.models import CharacterAction
from apps.game.exceptions import GameException
from apps.game.services.action.base_service import CharacterActionServicePrototype
from apps.game.services.character.core import CharacterService
from apps.game.services.world.movemant import MovementService


class CharacterActionPositionMoveService(CharacterActionServicePrototype):
    character_svc_cls = CharacterService

    def __init__(self, movement: MovementService):
        self.movement = movement

    def perform(self, action: CharacterAction):
        self.movement.move(action.initiator, action.position)
        action.perform()

    def check(self, action: CharacterAction):
        self.movement.validate_move(action.initiator, action.position)

    def check_acceptance(self, action: CharacterAction):
        # Character must have action points to move at least 1 point
        char_svc = self.character_svc_cls(action.initiator)
        if char_svc.get_current_ap() < 1:
            raise GameException("Not enough action points")
        if char_svc.get_current_hp() < 1:
            raise GameException("Character is dead")
        self.movement.validate_move(action.initiator, action.position)

    def accept(self, action: CharacterAction):
        self.check_acceptance(action)
        char_svc = self.character_svc_cls(action.initiator)
        char_svc.spend_all_ap()
