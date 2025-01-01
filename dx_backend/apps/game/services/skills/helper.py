from apps.character.models import Character
from apps.school.models import Skill, School


class CharacterSkillHelperService:
    """Manages skill-related operations for a Character."""

    def __init__(self, char: Character):
        self.char = char

    def learn_skills(self, skills: [Skill]) -> None:
        """Learn a list of skills."""
        for skill in skills:
            self.char.learned_skills.get_or_create(
                skill=skill,
                is_base=skill.school.is_base
            )

    def learn_all_skills(self, grade: int = 9) -> None:
        """Learn all skills of a given grade."""
        skills = Skill.objects.filter(grade=grade)
        self.learn_skills(skills)

    def forget_all_skills(self) -> None:
        """Forget all non-base skills."""
        self.char.learned_skills.exclude(is_base=True).delete()

    def learn_school(self, school: School) -> None:
        """Learn all skills of a specific school."""
        self.learn_skills(school.skills.filter(grade__gte=self.char.rank.grade))

    def learn_basics(self) -> None:
        """Learn the default 'basics' school."""
        base_schools = School.objects.filter(is_base=True)
        for school in base_schools:
            self.learn_school(school)

    @classmethod
    def fix_all_characters(cls) -> None:
        """Apply 'learn_basics' to all characters."""
        for char in Character.objects.all():
            cls(char).learn_basics()
