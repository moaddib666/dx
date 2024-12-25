import abc
import logging
import random

from apps.character.models import Character
from apps.world.models import Position
from ..character.character_clone import CharacterCloner


class SpawnRule(abc.ABC):
    @abc.abstractmethod
    def is_suitable_position(self, position: Position) -> bool:
        pass


class UndergroundMercenariesSpawnRule(SpawnRule):
    def is_suitable_position(self, position: Position) -> bool:
        """
        Checks if the position meets the spawn criteria:
        - grid_z = 0
        - labels list contains 'default' and 'enemy'
        """
        return position.grid_z == 0 and 'default' in position.labels and 'enemy' in position.labels


class AndroidsSpawnRule(SpawnRule):
    def is_suitable_position(self, position: Position) -> bool:
        """
        Checks if the position meets the spawn criteria:
        - grid_z = -1
        - labels list contains 'default' and 'enemy'
        """
        return position.grid_z == -1 and 'default' in position.labels and 'enemy' in position.labels


class Spawner(abc.ABC):
    clone_svc = CharacterCloner
    rules: list[SpawnRule]
    logger = logging.getLogger(__name__)

    def __init__(self, character: Character, min_count: int, max_count: int, rules: list[SpawnRule] = None):
        self.character = character
        self.cloner = self.clone_svc(character)
        self.min_count = min_count
        self.max_count = max_count
        self.validate()
        self.rules = rules or []
        self.logger.info(f"Spawner initialized with character {character.name} (ID: {character.id}), "
                         f"min_count={min_count}, max_count={max_count}, rules={rules}")

    def validate(self):
        if self.min_count < 0:
            self.logger.error("Validation error: min_count must be greater than or equal to 0")
            raise ValueError("min_count must be greater than or equal to 0")
        if self.max_count < 0:
            self.logger.error("Validation error: max_count must be greater than or equal to 0")
            raise ValueError("max_count must be greater than or equal to 0")
        if self.min_count > self.max_count:
            self.logger.error("Validation error: min_count must be less than or equal to max_count")
            raise ValueError("min_count must be less than or equal to max_count")

        self.logger.debug("Validation passed successfully.")

    def is_suitable_position(self, position: Position) -> bool:
        for rule in self.rules:
            if not rule.is_suitable_position(position):
                self.logger.debug(f"Position {position.id} is not suitable based on rule {rule.__class__.__name__}")
                return False
        self.logger.debug(f"Position {position.id} is suitable for all rules.")
        return True

    def spawn(self):
        self.logger.info("Starting the spawn process.")
        for position in Position.objects.all():
            try:
                if not self.is_suitable_position(position):
                    self.logger.debug(f"Skipping position {position.id} as it is not suitable.")
                    continue

                self.logger.info(f"Spawning characters at position {position.id}.")
                self.spawn_on_position(position)

            except Exception as e:
                self.logger.warning(f"Error while processing position {position.id}: {e}", exc_info=True)

    def spawn_on_position(self, position: Position):
        try:
            count = self.get_count()
            self.logger.info(f"Spawning {count} character(s) on position {position.id}.")
            for char in self.cloner.clone(count):
                self._move_character(char, position)
            self.logger.debug(f"Successfully spawned {count} character(s) on position {position.id}.")
        except Exception as e:
            self.logger.warning(f"Error spawning on position {position.id}: {e}", exc_info=True)

    def _move_character(self, char: Character, position: Position):
        try:
            char.position = position
            char.save()
            self.logger.debug(f"Moved character {char.name} (ID: {char.id}) to position {position.id}.")
        except Exception as e:
            self.logger.warning(f"Error moving character {char.id} to position {position.id}: {e}", exc_info=True)

    def get_count(self) -> int:
        count = random.randint(self.min_count, self.max_count)
        self.logger.debug(f"Generated spawn count: {count}")
        return count
