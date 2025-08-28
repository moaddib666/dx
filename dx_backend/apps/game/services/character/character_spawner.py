from apps.character.models import Character
from apps.world.models import Position


class CharacterSpawner:

    def spawn_character(self, character: Character, position: Position):
        character.position = position
        character.dimension_id = 1
        character.last_safe_position = position
        character.save(
            update_fields=[
                'position',
                'dimension_id',
                'last_safe_position'
            ]
        )
