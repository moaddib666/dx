from django.core.exceptions import ObjectDoesNotExist

from apps.character.models import Character
from apps.core.models import ItemType
from apps.world.models import Map


class AutoMapService:

    def map_characters(self):
        featured_characters = self.get_featured_characters()
        for character in featured_characters:
            self.add_character_position_to_map(character)

    def get_featured_characters(self) -> [Character]:
        return Character.objects.filter(
            is_active=True,
            equipped_items__world_item__item__type=ItemType.QUEST,
            equipped_items__world_item__item__name='Cartograph'
        ).distinct()

    def add_character_position_to_map(self, character: Character):
        character_position = character.position
        if not character.organization:
            return
        try:
            org_map = character.organization.map
        except ObjectDoesNotExist:
            org_map = Map.objects.create(
                name=f"World Map of {character.organization.name}",
                description=f"Map of {character.organization.name}",
                organization=character.organization
            )
        org_map.map_positions.get_or_create(
            position=character_position
        )
