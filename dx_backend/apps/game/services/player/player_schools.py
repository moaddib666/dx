from apps.game.exceptions import GameLogicException
from apps.player.models import Player
from apps.school.models import School
from apps.skills.models import LearnedSchool


class PlayerSchoolService:

    def initialize(self, player: Player):
        pass

    def add(self, player: Player, school: School) -> LearnedSchool:
        self.check_if_player_path_fits_school(player, school)
        self.check_if_player_has_school(player, school)
        self.check_if_max_schools_reached(player)
        return self._add_school_to_player(player, school)
    def check_if_player_path_fits_school(self, player, school):
        if not school.path.filter(pk=player.path.pk).exists():
            raise GameLogicException('Player path does not fit school path')

    def check_if_player_has_school(self, player, school):
        if player.learned_schools.filter(school=school).exists():
            raise GameLogicException('Player already has this school')

    def remove(self, player, learned_skill):
        learned_skill.delete()

    def check_if_max_schools_reached(self, player):
        if player.learned_schools.count() >= player.school_slots:
            raise GameLogicException('Player has reached the maximum number of schools')

    def _add_school_to_player(self, player, school) -> LearnedSchool:
        return player.learned_schools.create(school=school)
