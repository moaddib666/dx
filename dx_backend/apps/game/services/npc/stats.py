import logging
import typing as t

from apps.character.models import Character
from apps.core.models import CharacterStats

T_StatPriority = t.Tuple[CharacterStats, int]

magic_attacker_character_class = [
    (CharacterStats.FLOW_MANIPULATION, 5),
    (CharacterStats.KNOWLEDGE, 3),
    (CharacterStats.PHYSICAL_STRENGTH, 1),
    (CharacterStats.SPEED, 2),
]

physical_attacker_character_class = [
    (CharacterStats.PHYSICAL_STRENGTH, 5),
    (CharacterStats.SPEED, 3),
    (CharacterStats.KNOWLEDGE, 1),
    (CharacterStats.FLOW_MANIPULATION, 2),
]

balanced_character_class = [
    (CharacterStats.PHYSICAL_STRENGTH, 3),
    (CharacterStats.SPEED, 3),
    (CharacterStats.KNOWLEDGE, 3),
    (CharacterStats.FLOW_MANIPULATION, 3),
    (CharacterStats.FLOW_RESONANCE, 3),
    (CharacterStats.FLOW_CONNECTION, 3),
    (CharacterStats.LUCK, 1),
]


class StatsApplier:
    logger = logging.getLogger("services.npc.stats")

    def __init__(self, priorities: t.List[T_StatPriority]):
        self.priorities = priorities
        self.logger.info(f"StatsApplier initialized with priorities: {self.priorities}")

    def spend_stat_points(self, character: Character, points: int):
        """
        Spend points on stats based on the priorities
        """
        self.logger.info(f"Starting stat allocation for character: {character.name} with {points} points.")
        sum_priorities = sum(priority[1] for priority in self.priorities)
        if sum_priorities == 0:
            self.logger.warning("Sum of priorities is zero. No points will be allocated.")
            return

        points_per_priority = points // sum_priorities
        self.logger.debug(f"Calculated points per priority unit: {points_per_priority}")

        for stat_name, priority in self.priorities:
            additional_value = int(points_per_priority * priority)
            stat, _ = character.stats.get_or_create(name=stat_name)
            self.logger.debug(f"Allocating {additional_value} points to stat '{stat_name}' "
                              f"(current value: {stat.additional_value}).")
            stat.additional_value += additional_value
            stat.save(update_fields=['additional_value', 'updated_at'])
            points -= additional_value
            self.logger.info(f"{additional_value} points allocated to '{stat_name}'. Remaining points: {points}.")

        if points > 0:
            stat_name, _ = max(self.priorities, key=lambda x: x[1])
            stat, _ = character.stats.get_or_create(name=stat_name)
            self.logger.debug(f"Allocating remaining {points} points to highest priority stat '{stat_name}' "
                              f"(current value: {stat.additional_value}).")
            stat.additional_value += points
            stat.save(update_fields=['additional_value', 'updated_at'])
            self.logger.info(f"Remaining {points} points allocated to '{stat_name}'.")

        self.logger.info(f"Stat allocation complete for character: {character.name}.")
