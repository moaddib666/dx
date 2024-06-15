import logging

from apps.game.exceptions import GameLogicException
from apps.player.models import Player
from apps.world.models import Location


class LocationService:
    logger = logging.getLogger("game.services.location.LocationService")

    def __init__(self):
        pass

    def change_player_location(self, player: Player, location: Location):
        player_current_location = player.current_location

        self.logger.warning(f"Currently player able to teleport from any location to any location. ")

        # FIXME: movement logic
        if location.area == player_current_location.area:
            player.current_location = location
            player.save()
            self.logger.info(f"Player {player.name} changed his location from {player_current_location} to {location}")
            return

        raise GameLogicException("Player can't move to that location yet")
