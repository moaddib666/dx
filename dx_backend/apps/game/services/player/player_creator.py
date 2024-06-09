from apps.player.models import Character, Rank


class PlayerCreator:

    def __init__(self, client):
        self.client = client

    def create_player(self, name: str, age: int, gender: str) -> Character:
        rank, _ = Rank.objects.get_or_create(name='None', experience_needed=0)
        player = Character.objects.create(
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

        if not self.client.main_character:
            self.client.main_character = player
            self.client.save()

        return player
