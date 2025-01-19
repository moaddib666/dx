import logging

from apps.character.models import Character
from apps.core.models import BehaviorModel


class CharacterBehaviorService:
    logger = logging.getLogger("game.services.character.behavior")

    def __init__(self, character: Character):
        self.character = character
        self.logger.info(f"CharacterBehaviorService initialized for character {character.id} - {character.name}")

    def change_behavior(self, behavior: BehaviorModel):
        """
        Change the behavior of the character if it's an NPC.
        Logs the behavior change attempt and the result.
        """
        if not self.character.npc:
            self.logger.warning(
                f"Attempted to change behavior for non-NPC character {self.character.id} - {self.character.name}"
            )
            return
        if self.character.behavior == behavior:
            self.logger.debug(
                f"Character {self.character.id} - {self.character.name} already has behavior {behavior}"
            )
            return
        old_behavior = self.character.behavior
        self.character.behavior = behavior
        self.character.save(update_fields=["behavior"])
        self.logger.info(
            f"Character {self.character.id} - {self.character.name}: "
            f"Behavior changed from {old_behavior} to {behavior}"
        )

    def make_aggressive(self):
        """
        Change the character's behavior to AGGRESSIVE.
        """
        self.logger.debug(f"Making character {self.character.id} - {self.character.name} aggressive.")
        self.change_behavior(BehaviorModel.AGGRESSIVE)

    def make_friendly(self):
        """
        Change the character's behavior to FRIENDLY.
        """
        self.logger.debug(f"Making character {self.character.id} - {self.character.name} friendly.")
        self.change_behavior(BehaviorModel.FRIENDLY)

    def make_passive(self):
        """
        Change the character's behavior to PASSIVE.
        """
        self.logger.debug(f"Making character {self.character.id} - {self.character.name} passive.")
        self.change_behavior(BehaviorModel.PASSIVE)
