from apps.action.models import CharacterAction, DiceRollResult
from apps.core.models import CharacterStats, ImpactType, ImpactViolationType
from apps.game.exceptions import GameException
from apps.game.services.action.base_service import CharacterActionServicePrototype
from apps.game.services.character.core import CharacterService
from apps.game.services.rand_dice import DiceService


class DiceRollActionService(CharacterActionServicePrototype):
    character_svc_cls = CharacterService
    dice_svc_cls = DiceService

    def perform(self, action: CharacterAction):
        initiator = action.initiator
        char = self.character_svc_cls(initiator)
        luck = char.get_stat(CharacterStats.LUCK)
        svc = self.dice_svc_cls(initiator, sides=action.data["sides"], luck=luck)
        roll_result = svc.multiplier_roll()
        dice_result = DiceRollResult.objects.create(
            dice_side=roll_result.dice_side,
            multiplier=roll_result.multiplier,
            outcome=roll_result.outcome
        )
        self.create_impact(action, dice_result)
        action.perform()

    def create_impact(self, action: CharacterAction, result: DiceRollResult):
        action.impacts.create(
            target=action.initiator,
            type=ImpactType.NONE,
            violation=ImpactViolationType.NONE,
            size=result.dice_side,
            dice_roll_result=result
        )
        action.data["dice_result"] = result.dice_side
        action.save(update_fields=["data"])

    def check(self, action: CharacterAction):
        pass

    def check_acceptance(self, action: CharacterAction):
        if not action.data.get("sides"):
            raise GameException("Dice sides not provided")

    def accept(self, action: CharacterAction):
        self.check_acceptance(action)
        action.accept()
        self.perform(action)
