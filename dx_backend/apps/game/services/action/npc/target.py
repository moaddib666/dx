import abc
import random
import typing as t

from apps.game.services.action.npc.context import CharacterPositionActionContext
from apps.game.services.character.core import CharacterService


class TargetSelectionStrategy(abc.ABC):
    """
    Abstract service for selecting multiple targets using different strategies.
    Supports both attack and defense strategies with configurable target counts.
    """

    def __init__(self, context: CharacterPositionActionContext):
        self.context = context

    @abc.abstractmethod
    def calculate_target_count(self) -> int:
        """Calculate how many targets should be selected based on strategy."""
        pass

    @abc.abstractmethod
    def select_attack_targets(self) -> t.List[CharacterService]:
        """Select enemy targets for attack."""
        pass

    @abc.abstractmethod
    def select_defense_targets(self) -> t.List[CharacterService]:
        """Select friendly targets to defend."""
        pass

    def get_available_enemies(self) -> t.List[CharacterService]:
        """Get list of enemies that are not knocked out."""
        return [enemy for enemy in self.context.enemies if not enemy.is_knocked_out()]

    def get_available_friends(self) -> t.List[CharacterService]:
        """Get list of friends that are not knocked out."""
        return [friend for friend in self.context.friends if not friend.is_knocked_out()]

    def get_power_percentage(self, character: CharacterService) -> float:
        """Calculate power percentage: (current_power * 100) / max_power"""
        power_stats = character.get_power_stats()
        if power_stats.max_power == 0:
            return 0.0
        return (power_stats.current_power * 100) / power_stats.max_power


class TwoToOneStrategy(TargetSelectionStrategy):
    """
    Implements 2:1 strategy where for every 2 friends, we target 1 enemy.
    Examples:
    - 2 friends (ME + 1 FRIEND) = target 1 enemy
    - 4 friends (ME + 3 FRIENDS) = target 2 enemies
    """

    def calculate_target_count(self) -> int:
        """Calculate target count based on 2:1 ratio."""
        total_friends = len(self.context.friends) + 1  # +1 for ME
        return max(1, total_friends // 2)

    def select_attack_targets(self) -> t.List[CharacterService]:
        """Select strongest enemies up to the calculated target count."""
        available_enemies = self.get_available_enemies()
        target_count = min(self.calculate_target_count(), len(available_enemies))

        # Sort enemies by power (strongest first)
        sorted_enemies = sorted(
            available_enemies,
            key=lambda enemy: enemy.get_power_stats().max_power,
            reverse=True
        )

        return sorted_enemies[:target_count]

    def select_defense_targets(self) -> t.List[CharacterService]:
        """Select weakest friends that need protection."""
        available_friends = self.get_available_friends()
        target_count = min(self.calculate_target_count(), len(available_friends))

        # Sort friends by power (weakest first for defense priority)
        sorted_friends = sorted(
            available_friends,
            key=lambda friend: friend.get_power_stats().max_power
        )

        return sorted_friends[:target_count]


class AggressiveStrategy(TargetSelectionStrategy):
    """
    Aggressive strategy that targets as many enemies as possible.
    """

    def calculate_target_count(self) -> int:
        """Target all available enemies."""
        return len(self.get_available_enemies())

    def select_attack_targets(self) -> t.List[CharacterService]:
        """Select all available enemies, prioritizing strongest."""
        available_enemies = self.get_available_enemies()

        return sorted(
            available_enemies,
            key=lambda enemy: enemy.get_power_stats().max_power,
            reverse=True
        )

    def select_defense_targets(self) -> t.List[CharacterService]:
        """Select all friends that need protection."""
        return self.get_available_friends()


class DefensiveStrategy(TargetSelectionStrategy):
    """
    Defensive strategy that focuses on protecting friends.
    """

    def calculate_target_count(self) -> int:
        """Conservative target count - only target 1 enemy at a time."""
        return 1

    def select_attack_targets(self) -> t.List[CharacterService]:
        """Select single weakest enemy to minimize risk."""
        available_enemies = self.get_available_enemies()

        if not available_enemies:
            return []

        weakest_enemy = min(
            available_enemies,
            key=lambda enemy: enemy.get_power_stats().max_power
        )

        return [weakest_enemy]

    def select_defense_targets(self) -> t.List[CharacterService]:
        """Prioritize protecting the weakest friends."""
        available_friends = self.get_available_friends()

        return sorted(
            available_friends,
            key=lambda friend: friend.get_power_stats().max_power
        )


class ChaosMonkeyStrategy(TargetSelectionStrategy):
    """
    Chaos Monkey strategy that randomly selects targets.
    This is a fun and unpredictable strategy.
    """

    def calculate_target_count(self) -> int:
        """Randomly decide how many targets to select."""
        return random.randint(1, len(self.get_available_enemies()))

    def select_attack_targets(self) -> t.List[CharacterService]:
        """Randomly select enemies to attack."""
        available_enemies = self.get_available_enemies()
        target_count = self.calculate_target_count()

        return random.sample(available_enemies, min(target_count, len(available_enemies)))

    def select_defense_targets(self) -> t.List[CharacterService]:
        """Randomly select friends to defend."""
        available_friends = self.get_available_friends()
        target_count = self.calculate_target_count()

        return random.sample(available_friends, min(target_count, len(available_friends)))


class RandomSelectCompositeStrategy(TargetSelectionStrategy):
    """
    Randomly selects one of the available strategies.
    This allows for dynamic behavior in target selection.
    """

    def __init__(self, context: CharacterPositionActionContext, strategies: t.List[TargetSelectionStrategy]):
        super().__init__(context)
        self.strategies = strategies

    def calculate_target_count(self) -> int:
        return random.choice(self.strategies).calculate_target_count()

    def select_attack_targets(self) -> t.List[CharacterService]:
        """Select attack targets using a random strategy."""
        strategy = get_random_target_selection_strategy(self.context)
        return strategy.select_attack_targets()

    def select_defense_targets(self) -> t.List[CharacterService]:
        """Select defense targets using a random strategy."""
        random_strategy = get_random_target_selection_strategy(self.context)
        return random_strategy.select_defense_targets()


def get_random_target_selection_strategy(
        context: CharacterPositionActionContext
) -> TargetSelectionStrategy:
    strategies = [
        TwoToOneStrategy(context),
        AggressiveStrategy(context),
        DefensiveStrategy(context)
    ]

    return random.choice(strategies)
