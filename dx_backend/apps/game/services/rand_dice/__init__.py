import hashlib
import logging
import random
import time
from collections import Counter
from typing import Protocol

from apps.core.models import RollOutcome, DiceRollResult


class PlayerProtocol(Protocol):

    @property
    def id(self) -> str:
        ...


class DiceService:
    logger = logging.getLogger("game.services.dice")

    def __init__(self, player: PlayerProtocol, luck: int, sides: int = 6, base_luck: int = 5):
        self.player = player
        self.luck = luck
        self.sides = sides
        self.min_value = 1
        self.base_luck = base_luck
        self.random_gen = self.create_random_gen_for_player()
        self.logger.debug(f"Created dice service d{sides} for player {self.player.id} with luck {self.luck}")

    def create_random_gen_for_player(self):
        # Create a unique seed based on the player's unique ID and possibly other factors
        unique_string = str(self.player.id) + str(self.luck + time.time())
        seed = int(hashlib.md5(unique_string.encode()).hexdigest(), 16) % (2 ** 32 - 1)
        return random.Random(seed)

    def roll(self) -> int:

        base_roll = self.random_gen.randint(1, self.sides)
        # Adjust the roll based on luck
        luck_adjustment = (self.luck - self.base_luck) / self.base_luck * 1.3
        adjusted_roll = base_roll + (luck_adjustment * self.random_gen.randint(0, 1))
        adjusted_roll = max(self.min_value, min(self.sides, round(adjusted_roll)))
        self.logger.debug(f"Player {self.player.id} rolled {adjusted_roll} luck adjustment {luck_adjustment}")
        return adjusted_roll

    def _calculate_multiplier(self) -> tuple[int, float, RollOutcome]:
        """
        The multiplier is calculated as follows and adjusted by player's luck:
        - minValue  - Critical Fail (0.5) from the base value
        - maxValue  - Critical Success (2) from the base value
        - from middle - 1/2 to minValue of the base value - Bad luck (0.75)
        - from middle - 1/4 to - middle + 1/4  Base value (1)
        - from middle + 1/2 to maxValue of the base value - Good luck (1.25)
        """
        roll = self.roll()
        middle = (self.min_value + self.sides) / 2

        if roll == self.min_value:
            return roll, 0.5, RollOutcome.CRITICAL_FAIL
        elif roll == self.sides:
            return roll, 2.0, RollOutcome.CRITICAL_SUCCESS
        elif self.min_value < roll < middle - 0.5:
            return roll, 0.75, RollOutcome.BAD_LUCK
        elif middle - 0.25 <= roll <= middle + 0.25:
            return roll, 1.0, RollOutcome.BASE_VALUE
        elif middle + 0.5 < roll < self.sides:
            return roll, 1.25, RollOutcome.GOOD_LUCK
        else:
            return roll, 1.0, RollOutcome.BASE_VALUE  # This case shouldn't normally be reached

    def multiplier_roll(self) -> DiceRollResult:
        roll, multiplier, outcome = self._calculate_multiplier()
        self.logger.debug(f"Player {self.player.id} rolled {roll} with multiplier {multiplier} and outcome {outcome}")
        return DiceRollResult(dice_side=roll, multiplier=multiplier, outcome=outcome)


if __name__ == '__main__':
    def check_luck(luck: int, sides: int, count: int = 10_000):
        """
        Check the luck of the player
        """
        print(f"\n------------------------------------------\n"
              f"Checking luck for player with luck {luck} and dice with {sides} sides",
              "\n------------------------------------------")
        player = type("Player", (), {"id": "player_id"})
        dice_service = DiceService(player, luck, sides)
        outcome_results = Counter()

        for _ in range(count):
            roll, multiplier, outcome = dice_service.multiplier_roll()
            outcome_results[outcome] += 1

        # Print the results
        for outcome in RollOutcome:
            print(f"{outcome.value}: {outcome_results[outcome]} times")


    count = 100_000
    check_luck(5, 6, count)
    check_luck(10, 6, count)
    check_luck(15, 6, count)
    check_luck(20, 6, count)
