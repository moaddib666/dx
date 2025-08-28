from apps.action.models import CharacterAction, DiceRollResult
from apps.character.models import Character
from apps.core.models import CharacterStats, ImpactType, ImpactViolationType
from apps.game.exceptions import GameException
from apps.game.services.action.base_service import CharacterActionServicePrototype
from apps.game.services.character.core import CharacterService
from apps.game.services.rand_dice import DiceService


class DiceRollActionService(CharacterActionServicePrototype):
    character_svc_cls = CharacterService
    dice_svc_cls = DiceService
    default_difficulty = 12

    def perform(self, action: CharacterAction):
        initiator = action.initiator
        char = self.character_svc_cls(initiator)
        luck = char.get_stat(CharacterStats.LUCK)
        svc = self.dice_svc_cls(initiator, sides=action.data["sides"], luck=luck)
        difficulty = self.calculate_difficulty(initiator)
        challenge = action.challenge
        rolls_count = self.rolls_count(initiator)
        reduce_function = self.select_reduce_function(initiator)
        results = []
        for _ in range(rolls_count):
            roll_result = svc.challenge_roll(difficulty)
            dice_result = DiceRollResult.objects.create(
                dice_side=roll_result.dice_side,
                multiplier=roll_result.multiplier,
                outcome=roll_result.outcome
            )
            self.create_impact(action, dice_result)
            results.append(dice_result)

        target_result = reduce_function(results, key=lambda r: r.dice_side)

        action.perform()
        action.data["dice_result"] = target_result.dice_side
        action.save(update_fields=["data"])
        if challenge:
            challenge.outcome = target_result
            challenge.save(update_fields=["outcome_id"])
            initiator.challenge = None
            initiator.save(update_fields=["challenge_id"])

    def calculate_difficulty(self, initiator: "Character") -> int:
        if not initiator.challenge:
            return self.default_difficulty
        return initiator.challenge.difficulty

    def rolls_count(self, initiator: "Character") -> int:
        default = 1
        if not initiator.challenge:
            return default
        if initiator.challenge.advantage:
            return 2
        if initiator.challenge.disadvantage:
            return 1
        return default

    def select_reduce_function(self, initiator: "Character") -> callable:
        if not initiator.challenge:
            return max
        if initiator.challenge.advantage:
            return max
        if initiator.challenge.disadvantage:
            return min
        return max

    def create_impact(self, action: CharacterAction, result: DiceRollResult):
        action.impacts.create(
            target=action.initiator,
            type=ImpactType.NONE,
            violation=ImpactViolationType.NONE,
            size=result.dice_side,
            dice_roll_result=result
        )

    def check(self, action: CharacterAction):
        pass

    def check_acceptance(self, action: CharacterAction):
        if not action.data.get("sides"):
            raise GameException("Dice sides not provided")

    def accept(self, action: CharacterAction):
        self.check_acceptance(action)
