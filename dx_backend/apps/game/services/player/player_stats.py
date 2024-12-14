from apps.core.models import PlayerStat
from apps.player.models import Stat, Player


class PlayerStatsService:
    __default_stats_map__: dict[PlayerStat, int] = {
        PlayerStat.PHYSICAL_STRENGTH: 5,
        PlayerStat.MENTAL_STRENGTH: 5,
        PlayerStat.LUCK: 5,
        PlayerStat.SPEED: 5,
        PlayerStat.CONCENTRATION: 5,
        PlayerStat.FLOW_MANIPULATION: 0,
        PlayerStat.FLOW_CONNECTION: 0,
        PlayerStat.FLOW_RESONANCE: 0,
        PlayerStat.KNOWLEDGE: 0,
    }

    def initialize_stats(self, player: Player):
        for stat, value in self.__default_stats_map__.items():
            Stat.objects.get_or_create(player=player, name=stat, value=value)
