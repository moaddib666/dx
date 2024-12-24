import logging

from apps.game.exceptions import GameLogicException
from apps.character.models import Character
from apps.world.models import Location


class LocationService:
    logger = logging.getLogger("game.services.location.LocationService")

    def __init__(self):
        pass

    def change_character_location(self, character: Character, location: Location):
        character_current_location = character.current_location

        self.logger.warning(f"Currently character able to teleport from any location to any location. ")

        # FIXME: movement logic
        if location.area == character_current_location.area:
            character.current_location = location
            character.save()
            self.logger.info(f"Character {character.name} changed his location from {character_current_location} to {location}")
            return

        raise GameLogicException("Character can't move to that location yet")
