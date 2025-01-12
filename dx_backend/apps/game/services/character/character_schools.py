import uuid

from apps.character.models import Character
from apps.game.exceptions import GameLogicException
from apps.school.models import School, Skill
from apps.skills.models import LearnedSchool


class CharacterSchoolService:

    def initialize(self, character: Character, shools: list[uuid.UUID] = None) -> None:
        if shools is None:
            return
        for school_id in shools:
            school = School.objects.get(pk=school_id)
            self.add(character, school)
        self.enshure_know_basics(character)

    def enshure_know_basics(self, character: Character) -> None:
        basics_school = School.objects.get(id="3ea5c283-f8fd-4e24-a7e1-89ff96c8d796")
        self.add(character, basics_school)
        for skill in basics_school.skills.all():
            character.learned_skills.get_or_create(skill=skill, is_base=True)

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


class CharacterSchoolSkillService:
    """Service for managing skills and schools of a specific character."""

    def __init__(self, character: Character):
        self.character = character

    def learn_skills(self, skills: list[Skill]) -> None:
        """Teach the character a list of skills."""
        for skill in skills:
            self.character.learned_skills.get_or_create(skill=skill, is_base=skill.school.is_base)

    def learn_all_skills(self, grade: int = 9) -> None:
        """Teach the character all skills of a certain grade."""
        skills = Skill.objects.filter(grade=grade)
        self.learn_skills(skills)

    def forget_all_skills(self) -> None:
        """Remove all skills from the character, except base skills."""
        self.character.learned_skills.exclude(is_base=True).delete()

    def learn_school(self, school: School, grade: int = None) -> None:
        """Teach the character all skills from a school."""
        grade = grade or self.character.rank.grade  # Use character's grade if not provided
        skills = school.skills.filter(grade__gte=grade)
        self.character.learned_schools.get_or_create(school=school)
        self.learn_skills(skills)

    def learn_basics(self) -> None:
        """Teach the character basic skills from the basics school."""
        basics_school = School.objects.get(id="3ea5c283-f8fd-4e24-a7e1-89ff96c8d796")
        self.learn_school(basics_school)
