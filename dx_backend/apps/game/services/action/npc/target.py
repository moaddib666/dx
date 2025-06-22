import abc
import typing as t

from apps.game.services.action.npc.context import CharacterPositionActionContext
from apps.game.services.character.core import CharacterService


class TargetSelectorService(abc.ABC):
    """
    Service for selecting targets based on the current context of the character.
    """

    def __init__(self, context: CharacterPositionActionContext):
        self.context = context

    @abc.abstractmethod
    def select_target(self) -> t.Optional[CharacterService]:
        pass


class TargetSelectionStrategyService(abc.ABC):
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


class TwoToOneStrategyService(TargetSelectionStrategyService):
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


class AggressiveStrategyService(TargetSelectionStrategyService):
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


class DefensiveStrategyService(TargetSelectionStrategyService):
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


class EnemyTargetSelectorService(TargetSelectorService):
    """
    Service for selecting an enemy target based on the current context of the character.
    Updated to work with the strategy service.
    """

    def __init__(self, context: CharacterPositionActionContext, strategy: TargetSelectionStrategyService = None):
        super().__init__(context)
        self.strategy = strategy or TwoToOneStrategyService(context)

    def calculate_target_pool_size(self) -> int:
        """
        Count of enemies to choose from. Based on enemy and friends count.
        Uses the configured strategy to determine target count.
        """
        return self.strategy.calculate_target_count()

    def select_target(self) -> t.Optional[CharacterService]:
        """Select single target using strategy."""
        targets = self.strategy.select_attack_targets()
        return targets[0] if targets else None

    def select_multiple_targets(self) -> t.List[CharacterService]:
        """Select multiple targets using strategy."""
        return self.strategy.select_attack_targets()

    def choose_target(self, target1: CharacterService, target2: CharacterService) -> CharacterService:
        """Choose between two targets based on power."""
        power1 = target1.get_power_stats()
        power2 = target2.get_power_stats()
        if power1.max_power < power2.max_power:
            return target2
        return target1
