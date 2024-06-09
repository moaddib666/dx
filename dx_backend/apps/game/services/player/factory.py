from django.db import transaction
from .player_creator import PlayerCreator
from .location_service import LocationService
from .player_spawner import PlayerSpawner
from .player_stats import PlayerStatsService


class PlayerFactory:

    def __init__(self, client):
        self.client = client
        self.player_creator = PlayerCreator(self.client)
        self.location_service = LocationService()
        self.player_spawner = PlayerSpawner()
        self.player_stats = PlayerStatsService()

    def create_player(self, name: str, age: int, gender: str):
        player = self.player_creator.create_player(name, age, gender)
        location = self.location_service.get_or_create_home_location(player)
        self.player_spawner.spawn_player(player, location)
        self.player_stats.initialize_stats(player)
        return player
