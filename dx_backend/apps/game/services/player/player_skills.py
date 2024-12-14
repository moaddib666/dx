from apps.game.exceptions import GameLogicException
from apps.player.models import Player
from apps.school.models import Skill
from apps.skills.models import LearnedSkill

class PlayerSkillsService:

    def initialize(self, player: Player):
        pass

    def add(self, player: Player, skill: Skill) -> LearnedSkill:
        self.check_if_player_has_skill(player, skill)
        self.check_if_max_skills_reached(player)
        self.check_if_player_has_required_school(player, skill)
        self.check_if_player_has_required_level(player, skill)

        return self._add_skill_to_player(player, skill)

    def check_if_player_has_skill(self, player, skill):
        if player.learned_skills.filter(skill=skill).exists():
            raise GameLogicException('Player already has this skill')

    def check_if_max_skills_reached(self, player):
        max_skills = 3 + player.rank_grade.grade  # TODO: refine this formula
        if player.learned_skills.count() >= max_skills:
            raise GameLogicException('Player has reached the maximum number of skills')

    def check_if_player_has_required_school(self, player, skill):
        player_schools = player.learned_schools.filter(school=skill.school)
        if not player_schools.exists():
            raise GameLogicException('Player does not have the required school')

    def check_if_player_has_required_level(self, player, skill):
        if player.rank_grade.grade < skill.grade:
            raise GameLogicException('Player does not have the required level')

    def _add_skill_to_player(self, player, skill) -> LearnedSkill:
        return player.learned_skills.create(skill=skill)

    def remove(self, player, learned_skill):
        learned_skill.delete()

