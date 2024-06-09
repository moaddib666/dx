from apps.player.models import Player, Rank


class PlayerCreator:

    def __init__(self, client):
        self.client = client

    def create_player(self, name: str, age: int, gender: str) -> Player:
        rank = Rank.objects.filter(grade=0).order_by('experience_needed').first()
        player = Player.objects.create(
            owner=self.client,
            name=name,
            age=age,
            gender=gender,
            bio='New player character.',
            organization=None,  # Set as needed
            rank=rank,
            experience=0,
            current_health_points=50,
            current_energy_points=0,
            current_active_points=10,
        )

        if not self.client.player:
            self.client.player = player
            self.client.save()

        return player
