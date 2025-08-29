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
            organization=None,  # Set as needed
            rank=rank,
            experience=0,
            current_health_points=50,
            current_energy_points=0,
            current_active_points=10,
            campaign=self.client.current_campaign,
        )

        # Map gender to appropriate avatar
        gender_avatar_map = {
            'Male': 'avatars/placeholder/male.png',
            'Female': 'avatars/placeholder/female.png',
            'Other': 'avatars/placeholder/other.png',
        }
        avatar_path = gender_avatar_map.get(gender, 'avatars/placeholder/other.png')
        
        # Create CharacterBiography with gender and appropriate avatar
        CharacterBiography.objects.create(
            age=age,
            gender=gender,
            background='',
            appearance='',
            avatar=avatar_path,
            character=character,
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
            is_active=True,
            campaign=self.client.current_campaign,
        )
        character.position = position
        character.save()
        
        # Map gender to appropriate avatar
        gender_avatar_map = {
            'Male': 'avatars/placeholder/male.png',
            'Female': 'avatars/placeholder/female.png',
            'Other': 'avatars/placeholder/other.png',
        }
        avatar_path = gender_avatar_map.get(dto.bio.gender, 'avatars/placeholder/other.png')
        
        CharacterBiography(
            age=dto.bio.age,
            gender=dto.bio.gender,
            background=dto.bio.background,
            appearance=dto.bio.appearance,
            avatar=avatar_path,
            character=character,
        ).save()
        return character
