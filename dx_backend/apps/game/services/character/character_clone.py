import typing
from copy import deepcopy
from django.db import transaction

from apps.character.models import (
    Character, Stat, CharacterBiography, StatModifier
)

from apps.skills.models import (
    LearnedSkill, LearnedSchool
)

class CharacterCloner:
    def __init__(self, char: Character):
        self.char = char

    def clone(self, count: int, template: str = "{base_name} {index}") -> typing.Iterable[Character]:
        clones = []
        for i in range(count):
            with transaction.atomic():
                new_char = Character.objects.create(
                    owner=self.char.owner,
                    name=template.format(base_name=self.char.name, index=i + 1),
                    organization=self.char.organization,
                    tags=deepcopy(self.char.tags),
                    path=self.char.path,
                    rank=self.char.rank,
                    experience=self.char.experience,
                    current_health_points=self.char.current_health_points,
                    current_energy_points=self.char.current_energy_points,
                    current_active_points=self.char.current_active_points,
                    place_of_birth=self.char.place_of_birth,
                    fight=self.char.fight,
                    school_slots=self.char.school_slots,
                    npc=self.char.npc,
                    behavior=self.char.behavior,
                    last_safe_position=self.char.last_safe_position,
                    resetting_base_stats=self.char.resetting_base_stats,
                    dimension=self.char.dimension,
                    is_active=self.char.is_active,
                    campaign=self.char.campaign,
                    position=self.char.position  # Copy position
                )
                # Clone related attributes
                self.clone_stats(self.char, new_char)
                self.clone_stat_modifiers(self.char, new_char)
                self.clone_biography(self.char, new_char)
                self.clone_learned_skills(self.char, new_char)
                self.clone_learned_schools(self.char, new_char)

                clones.append(new_char)
        return clones

    def clone_stats(self, source: Character, target: Character) -> None:
        for stat in source.stats.all():
            Stat.objects.create(
                character=target,
                name=stat.name,
                base_value=stat.base_value,
                additional_value=stat.additional_value
            )

    def clone_stat_modifiers(self, source: Character, target: Character) -> None:
        for modifier in source.stats_modifiers.filter(applied_by_effect__isnull=True):
            StatModifier.objects.create(
                character=target,
                name=modifier.name,
                value=modifier.value
            )

    def clone_biography(self, source: Character, target: Character) -> None:
        if hasattr(source, 'biography') and source.biography:
            CharacterBiography.objects.create(
                character=target,
                age=source.biography.age,
                gender=source.biography.gender,
                background=source.biography.background,
                appearance=source.biography.appearance,
                avatar=source.biography.avatar
            )

    def clone_learned_skills(self, source: Character, target: Character) -> None:
        for learned_skill in source.learned_skills.all():
            LearnedSkill.objects.create(
                character=target,
                skill=learned_skill.skill,
                is_base=learned_skill.is_base
            )

    def clone_learned_schools(self, source: Character, target: Character) -> None:
        for learned_school in source.learned_schools.all():
            LearnedSchool.objects.create(
                character=target,
                school=learned_school.school,
                is_base=learned_school.is_base
            )
