from apps.player.models import Character
from apps.world.models import  Location


class PlayerSpawner:

    def spawn_player(self, player: Character, location: Location):
        player.current_location = location
        player.place_of_birth = location  # TODO: make dynamic Assuming the place of birth is the same as the starting location
        player.dimension_id = 1
        player.save()
