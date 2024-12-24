import logging
import uuid

from apps.character.models import Character
from apps.game.exceptions import GameLogicException
from apps.modificators.models import Modificator, CharacterModificator


class CharacterModificatorService:
    logger = logging.getLogger(__name__)

    def initialize(self, character: Character, modificators: list[uuid.UUID] = None) -> None:
        if modificators is None:
            return
        for modificator_id in modificators:
            modificator = Modificator.objects.get(pk=modificator_id)
            self.add(character, modificator)

    def add(self, character: Character, modificator: Modificator) -> CharacterModificator:
        self.check_if_character_has_modificator(character, modificator)
        self.check_if_max_modificators_reached(character)
        return self._add_modificator_to_character(character, modificator)

    def check_if_character_has_modificator(self, character, modificator):
        if character.modificators.filter(modificator=modificator).exists():
            raise GameLogicException('Character already has this modificator')

    def remove(self, character, applied_modificator: CharacterModificator):
        applied_modificator.delete()

    def check_if_max_modificators_reached(self, character):
        if character.modificators.count() >= 2:
            raise GameLogicException('Character has reached the maximum number of modificators')

    def _add_modificator_to_character(self, character, modificator: Modificator) -> CharacterModificator:
        for stat_modificator in modificator.statmodificator_set.all():
            try:
                charecter_stat = character.stats.get(name=stat_modificator.stat)
                charecter_stat.value += stat_modificator.value
                charecter_stat.save(update_fields=['value'])
            except Exception as e:
                self.logger.warning(f'Failed to apply modificator {modificator} to character {character}: {e}')

        return character.modificators.create(modificator=modificator)
