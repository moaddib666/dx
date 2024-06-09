from apps.player.models import Player


class PlayerService:
    def __init__(self, player: Player):
        self.player = player

    def get_player_info(self):
        self.player.refresh_from_db()
        return {
            'id': self.player.id,
            'name': self.player.name,
            'stats': {
                'health': self.player.current_health_points,
                'max_health': self.player.stats.health_points,
                'energy': self.player.current_energy_points,
                'max_energy': self.player.stats.energy_points,
                'ap': self.player.current_active_points,
                'max_ap': int(round(self.player.stats.speed * 0.5 * self.player.dimension.speed)),
            },
            'location': {
                'id': self.player.current_location.id,
                'name': self.player.current_location.name,
            },
            "dimension": {
                "number": self.player.dimension.id,
                "speed": self.player.dimension.speed,
                "energy": self.player.dimension.energy,
            },
            'rank': {
                'name': self.player.rank.name,
                'experience': self.player.experience,
                'next_rank_experience': self.player.rank.experience_needed,
            },
            'active_effects': [],
        }

