import logging
from apps.game.dto.impact import CalculatedImpact
from apps.game.exceptions import GameLogicException
from apps.game.services.player.core import PlayerService
from apps.school.dto import Impact
from apps.school.models import Skill
from typing import List, Dict, Any


class SkillImpactService:
    logger = logging.getLogger("game.services.skill_impact")

    def __init__(self, skill: Skill, player: PlayerService):
        self.initiator = player
        self.skill = skill

    def calculate_impact(self) -> List[CalculatedImpact]:
        self.logger.info(f"Calculating impact for skill {self.skill.id} used by player {self.initiator.player.id}")

        if self.skill.type != Skill.Types.ATTACK:
            self.logger.error("Only attack skills supported for now")
            raise GameLogicException("Only attack skills supported for now")

        impacts: List[Impact] = self.skill.impact
        calculated_impacts = [self.calculate_damage(impact) for impact in impacts]

        return calculated_impacts

    def calculate_damage(self, impact: Impact) -> CalculatedImpact:
        """
        The formula in impact looks like this:
        {
            "base": 15,
            "requires": [{"stat": "Flow Manipulation", "value": 5}],
            "scaling": [{"stat": "Flow Manipulation", "value": 0.2}]
        }
        """
        self.logger.info(f"Calculating damage for impact {impact['kind']}")

        formula = impact['formula']
        base_damage = formula.get("base", 0)
        required_stats = formula.get("requires", [])
        scaling_factors = formula.get("scaling", [])
        damage = base_damage
        self.logger.debug(f"Base damage: {base_damage}")

        # Apply penalties for not meeting required stats
        for stat in required_stats:
            current_level = self.initiator.get_stat(stat["stat"])
            required_level = stat["value"]
            self.logger.debug(
                f"Checking required stat {stat['stat']}: current level {current_level}, required level {required_level}")
            if current_level < required_level:
                penalty_factor = (required_level - current_level) / required_level
                damage *= (1 - penalty_factor)
                self.logger.debug(
                    f"Applied penalty for stat {stat['stat']}: penalty factor {penalty_factor}, new damage {damage}")

        # Apply scaling factors
        for scaling in scaling_factors:
            scaling_stat = scaling["stat"]
            scaling_value = scaling["value"]
            current_level = self.initiator.get_stat(scaling_stat)
            self.logger.debug(
                f"Applying scaling factor for stat {scaling_stat}: scaling value {scaling_value}, current level {current_level}")
            damage *= (1 + scaling_value * current_level)
            self.logger.debug(f"New damage after scaling: {damage}")

        self.logger.info(f"Final calculated damage: {damage}")
        return CalculatedImpact(kind=impact['kind'], value=damage)
