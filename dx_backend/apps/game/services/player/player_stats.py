from apps.player.models import CharacterStatSet


class PlayerStatsService:

    def initialize_stats(self, player):
        return CharacterStatSet.objects.create(
            health_points=50,
            energy_points=0,
            physical_strength=10,
            mental_strength=10,
            luck=10,
            speed=10,
            concentration=0,
            flow_manipulation=0,
            flow_connection=0,
            knowledge=0,
            flow_resonance=0
        )
