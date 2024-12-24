from apps.character.models import Character
from apps.world.models import Position


class CharacterSpawner:

    def spawn_character(self, character: Character, location: Position):
        character.position = location
        character.dimension_id = 1
        character.save(
            update_fields=[
                'position',
                'dimension_id',
            ]
        )
