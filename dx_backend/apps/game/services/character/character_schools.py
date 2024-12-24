import uuid

from apps.character.models import Character
from apps.game.exceptions import GameLogicException
from apps.school.models import School
from apps.skills.models import LearnedSchool


class CharacterSchoolService:

    def initialize(self, character: Character, shools: list[uuid.UUID] = None) -> None:
        if shools is None:
            return
        for school_id in shools:
            school = School.objects.get(pk=school_id)
            self.add(character, school)

    def add(self, character: Character, school: School) -> LearnedSchool:
        self.check_if_character_path_fits_school(character, school)
        self.check_if_character_has_school(character, school)
        self.check_if_max_schools_reached(character)
        return self._add_school_to_character(character, school)

    def check_if_character_path_fits_school(self, character, school):
        if not school.path.filter(pk=character.path.pk).exists():
            raise GameLogicException('Character path does not fit school path')

    def check_if_character_has_school(self, character, school):
        if character.learned_schools.filter(school=school).exists():
            raise GameLogicException('Character already has this school')

    def remove(self, character, learned_skill):
        learned_skill.delete()

    def check_if_max_schools_reached(self, character):
        if character.learned_schools.count() >= character.school_slots:
            raise GameLogicException('Character has reached the maximum number of schools')

    def _add_school_to_character(self, character, school) -> LearnedSchool:
        return character.learned_schools.create(school=school)
