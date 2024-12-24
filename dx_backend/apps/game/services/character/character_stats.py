from apps.character.models import Stat, Character
from apps.core.models import CharacterStats, CharacterStatHolder


class CharacterStatsService:
    __default_stats_map__: dict[CharacterStats, int] = {
        CharacterStats.PHYSICAL_STRENGTH: 5,
        CharacterStats.MENTAL_STRENGTH: 5,
        CharacterStats.LUCK: 5,
        CharacterStats.SPEED: 5,
        CharacterStats.CONCENTRATION: 5,
        CharacterStats.FLOW_MANIPULATION: 0,
        CharacterStats.FLOW_CONNECTION: 0,
        CharacterStats.FLOW_RESONANCE: 0,
        CharacterStats.KNOWLEDGE: 0,
    }
    statModel = Stat

    def initialize_stats(self, character: Character):
        for stat, value in self.__default_stats_map__.items():
            self.statModel.objects.get_or_create(character=character, name=stat, value=value)

    def import_stats(self, character: Character, stats: list[CharacterStatHolder]):
        for stat in stats:
            self.statModel.objects.get_or_create(character=character, name=stat.name, value=stat.value)
