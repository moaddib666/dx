from apps.action.models import DiceRollResult
from apps.character.models import Stat, Character
from apps.core.models import CharacterStats
from apps.game.services.rand_dice import DiceService


class CharacterBaseStatsService:
    statModel = Stat
    diceRollModel = DiceRollResult
    roll_count = 4
    roll_sides = 4

    def __init__(self, char: Character, dice_service: type[DiceService]):
        self.char = char
        self.dice_service = dice_service(
            char,
            10
        )

    def reset_base_stats(self) -> [Stat]:
        stats = []
        for stat_name in CharacterStats:
            stats.append(self.generate_base_stat(stat_name))
        return stats

    def generate_base_stat(self, stat: CharacterStats) -> Stat:
        character_stat, created = self.statModel.objects.update_or_create(
            character=self.char,
            name=stat
        )
        if not created:
            character_stat.dice_rolls.clear()
        rolls = self.generate_stat_rolls(stat)
        character_stat.dice_rolls.add(*rolls)
        # set the base value to the sum of the remaining rolls
        character_stat.base_value = int(sum([roll.dice_side for roll in rolls]) - min(rolls, key=lambda x: x.dice_side).dice_side)
        character_stat.save(
            update_fields=['base_value', 'updated_at']
        )
        return character_stat

    def generate_stat_rolls(self, stat: CharacterStats) -> [DiceRollResult]:
        dice_results = []
        for _ in range(self.roll_count):
            die_roll = self.dice_service.multiplier_roll()
            dice_results.append(
                self.diceRollModel.objects.create(
                    dice_side=die_roll.dice_side,
                    multiplier=die_roll.multiplier,
                    outcome=die_roll.outcome
                )
            )
        return dice_results

    def switch_base_stats(self, stat_1: Stat, stat_2: Stat):
        """
        Switches the results of two base stat generations.

        Take roles from stat_1 and stat_2 and switch them.
        Take base values from stat_1 and stat_2 and switch them.
        """
        # ensure stat 1 and stat 2 is from the same character
        if stat_1.character != stat_2.character or stat_1.character != self.char:
            raise ValueError("The stats must be from the same character.")

        rolls_1 = list(stat_1.dice_rolls.all())
        rolls_2 = list(stat_2.dice_rolls.all())

        stat_1.dice_rolls.clear()
        stat_2.dice_rolls.clear()

        stat_1.dice_rolls.add(*rolls_2)
        stat_2.dice_rolls.add(*rolls_1)

        stat_1.base_value, stat_2.base_value = stat_2.base_value, stat_1.base_value
        stat_1.save(update_fields=['base_value', 'updated_at'])
        stat_2.save(update_fields=['base_value', 'updated_at'])
