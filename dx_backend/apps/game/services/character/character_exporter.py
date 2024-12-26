from typing import List

from apps.character.models import Character
from apps.core.models import CharacterGenericData, CharacterStatHolder, CharacterBio


class CharacterExportService:
    def export_character(self, character: Character) -> CharacterGenericData:
        # Fetch related stats and other details
        stats = [
            CharacterStatHolder(name=stat.name, value=stat.value)
            for stat in character.stats.all()
        ]

        # Fetch modificators (placeholder, update based on your logic)
        modificators = [modifier.id for modifier in character.modificators.all()]

        # Fetch items (placeholder, update based on your logic)
        # items = [item.id for item in character.items.all()]
        items = []
        # Fetch schools (placeholder, update based on your logic)
        schools = [school.id for school in character.learned_schools.all()]

        # Fetch spells (placeholder, update based on your logic)
        spells = [spell.skill_id for spell in character.learned_skills.all()]

        # Fetch biography details
        biography = character.biography
        character_bio = CharacterBio(
            age=biography.age,
            gender=biography.gender,
            appearance=biography.appearance,
            background=biography.background,
        )

        # Fetch rank details
        rank = character.rank

        return CharacterGenericData(
            name=character.name,
            tags=character.tags,
            bio=character_bio,
            rank=rank.grade if rank else 9,
            path=character.path.id if character.path else None,
            stats=stats,
            modificators=modificators,
            items=items,
            schools=schools,
            spells=spells,
        )

    def export_all_characters(self) -> List[CharacterGenericData]:
        characters = Character.objects.prefetch_related(
            'stats', 'biography', 'rank', 'path', 'modificators', 'learned_schools', 'learned_skills'
        )
        # TODO: items
        return [self.export_character(character) for character in characters]

    def to_json(self, character: Character, **kwargs) -> str:
        data = self.export_character(character)
        return data.model_dump_json(**kwargs)


if __name__ == '__main__':
    character_id = 'e1cd95a3-bd01-4e57-aefa-2e83144406d9'
    char = Character.objects.get(pk=character_id)
    service = CharacterExportService()
    print(service.to_json(char, indent=2))
