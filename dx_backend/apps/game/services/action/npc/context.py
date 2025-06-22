import typing as t
from dataclasses import dataclass

from apps.game.services.action.npc.position import logger
from apps.game.services.character.core import CharacterService

logger = logger.getChild(__name__)


@dataclass
class CharacterPositionActionContext:
    character: CharacterService
    friends: t.Set[CharacterService]
    enemies: t.Set[CharacterService]
    neutral: t.Set[CharacterService]

    def add_friend(self, friend: CharacterService):
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
