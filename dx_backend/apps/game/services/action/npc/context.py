import logging
import typing as t
from dataclasses import dataclass

from apps.game.services.character.core import CharacterService

logger = logging.getLogger("game.service.npc.context")


@dataclass
class CharacterPositionActionContext:
    character: CharacterService
    friends: t.Set[CharacterService]
    enemies: t.Set[CharacterService]
    neutral: t.Set[CharacterService]

    def is_self(self, character: CharacterService) -> bool:
        """
        Check if the given character is not the same as the character in this context.
        """
        logger.debug(f"Checking if {character} is not self for {self.character}")
        return self.character.get_id() == character.get_id()

    def add_friend(self, friend: CharacterService):
        if self.is_self(friend):
            logger.debug(f"Skipping adding self {friend} to friends list")
            return
        logger.debug(f"Attempting to add friend {friend} to character {self.character}")
        if friend in self.enemies:
            logger.debug(f"Friend {friend} is in enemies list, skipping")
            return
        if friend in self.neutral:
            logger.debug(f"Removing {friend} from neutral list")
            self.neutral.remove(friend)
        if friend not in self.friends:
            logger.debug(f"Adding {friend} to friends list")
            self.friends.add(friend)
        else:
            logger.debug(f"{friend} already in friends list")

    def add_enemy(self, enemy: CharacterService):
        if self.is_self(enemy):
            logger.debug(f"Skipping adding self {enemy} to enemies list")
            return
        logger.debug(f"Attempting to add enemy {enemy} to character {self.character}")
        if enemy not in self.enemies:
            logger.debug(f"Adding {enemy} to enemies list")
            self.enemies.add(enemy)
        else:
            logger.debug(f"{enemy} already in enemies list")
        if enemy in self.friends:
            logger.debug(f"Removing {enemy} from friends list")
            self.friends.remove(enemy)
        if enemy in self.neutral:
            logger.debug(f"Removing {enemy} from neutral list")
            self.neutral.remove(enemy)

    def add_neutral(self, neutral: CharacterService):
        if self.is_self(neutral):
            logger.debug(f"Skipping adding self {neutral} to neutral list")
            return
        logger.debug(f"Attempting to add neutral {neutral} to character {self.character}")
        if neutral in self.enemies:
            logger.debug(f"Neutral {neutral} is in enemies list, skipping")
            return
        if neutral in self.friends:
            logger.debug(f"Neutral {neutral} is in friends list, skipping")
            return
        if neutral not in self.neutral:
            logger.debug(f"Adding {neutral} to neutral list")
            self.neutral.add(neutral)
        else:
            logger.debug(f"{neutral} already in neutral list")
