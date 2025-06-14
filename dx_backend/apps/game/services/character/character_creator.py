from apps.character.models import Character, Rank, CharacterBiography
from apps.core.models import CharacterGenericData
from apps.world.models import Position


class CharacterCreator:

    def __init__(self, client):
        self.client = client

    def create_character(self, name: str, age: int, gender: str) -> Character:
        rank = Rank.objects.filter(grade=0).order_by('experience_needed').first()
        # FIXME: Not working as expected
        character = Character.objects.create(
            owner=self.client,
            name=name,
            age=age,
            gender=gender,
            organization=None,  # Set as needed
            rank=rank,
            experience=0,
            current_health_points=50,
            current_energy_points=0,
            current_active_points=10,
        )

        if not self.client.main_character:
            self.client.main_character = character
            self.client.save()

        return character

    def import_character(self, dto: CharacterGenericData):
        # FIXME: Rank must be taken from the dto.rank field an resolved to the Rank object
        # Rank__id = c9a67bf5-76e0-4f89-b06b-2ab1d9aa4a3f // 9th grade
        position = Position.objects.filter(
            grid_z=1,
            is_safe=True,
        ).first()
        character = Character(
            owner=self.client,
            name=dto.name,
            rank_id='c9a67bf5-76e0-4f89-b06b-2ab1d9aa4a3f',
            path_id=dto.path,
            tags=dto.tags,
            is_active=False,
        )
        character.position = position
        character.save()
        CharacterBiography(
            age=dto.bio.age,
            background=dto.bio.background,
            appearance=dto.bio.appearance,
            character=character,
        ).save()
        return character
