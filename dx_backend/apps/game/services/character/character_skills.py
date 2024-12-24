import uuid

from apps.character.models import Character
from apps.game.exceptions import GameLogicException
from apps.school.models import Skill
from apps.skills.models import LearnedSkill


class CharacterSkillsService:

    def initialize(self, character: Character, skills: list[uuid] = None) -> None:
        if skills is None:
            return
        for skill_id in skills:
            skill = Skill.objects.get(pk=skill_id)
            self.add(character, skill)

    def add(self, character: Character, skill: Skill) -> LearnedSkill:
        self.check_if_character_has_skill(character, skill)
        self.check_if_max_skills_reached(character)
        self.check_if_character_has_required_school(character, skill)
        self.check_if_character_has_required_level(character, skill)

        return self._add_skill_to_character(character, skill)

    def check_if_character_has_skill(self, character, skill):
        if character.learned_skills.filter(skill=skill).exists():
            raise GameLogicException('Character already has this skill')

    def check_if_max_skills_reached(self, character):
        max_skills = 3 + character.rank.grade  # TODO: refine this formula
        if character.learned_skills.count() >= max_skills:
            raise GameLogicException('Character has reached the maximum number of skills')

    def check_if_character_has_required_school(self, character, skill):
        character_schools = character.learned_schools.filter(school=skill.school)
        if not character_schools.exists():
            raise GameLogicException('Character does not have the required school')

    def check_if_character_has_required_level(self, character, skill):
        if character.rank.grade < skill.grade:
            raise GameLogicException('Character does not have the required level')

    def _add_skill_to_character(self, character, skill) -> LearnedSkill:
        return character.learned_skills.create(skill=skill)

    def remove(self, character, learned_skill):
        learned_skill.delete()
