from apps.game.exceptions import GameLogicException
from apps.game.services.action.base_service import BaseService
from apps.game.services.skills.cost_validator import SkillCostService


class SkillActionService(BaseService):

    def run(self):
        raise NotImplementedError

    def check(self):
        self.check_skill_capability()
        self.check_target_capability()

    def check_skill_capability(self):
        # check player has skill in equipted skills
        self.initiator.has_skill(self.action.skill_id)
        skill = self.action.skill

        SkillCostService(skill).apply(self.initiator.player)

        # check skill has valid target
        if not skill.multi_target and len(self.target) > 1:
            raise GameLogicException("Skill is not multi target")
        # check defense skill applied to self or ally

        suitable_targets = []
        if skill.is_defense() or skill.is_buff() or skill.is_heal():
            for ally in self.get_allys().filter(id__in=[target.player.id for target in self.target]):
                suitable_targets.append(ally)
        if skill.is_attack() or skill.is_debuff():
            if self.initiator.player.fight is None:
                raise GameLogicException("Player not in fight")
            for enemy in self.get_enemies().filter(id__in=[target.player.id for target in self.target]):
                suitable_targets.append(enemy)

        if not suitable_targets:
            raise GameLogicException("No suitable targets")

    def get_allys(self):
        fight = self.initiator.player.fight
        if self.initiator.player in fight.side_a_participants.filter(id=self.initiator.player.id):
            return fight.side_a_participants
        return fight.side_b_participants

    def get_enemies(self):
        fight = self.initiator.player.fight
        if self.initiator.player in fight.side_a_participants.filter(id=self.initiator.player.id):
            return fight.side_b_participants
        return fight.side_a_participants

    def check_target_capability(self):
        suitable_targets = []
        for target in self.target:
            if target.player.fight != self.initiator.player.fight:
                continue
            suitable_targets.append(target)
            # check if target is in same or same -1 dimension
            if not (target.player.dimension_id == self.initiator.player.dimension_id \
                    or target.player.dimension_id == (self.initiator.player.dimension_id - 1)):
                continue

        if not suitable_targets:
            raise GameLogicException("No suitable targets")
