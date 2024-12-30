import logging
from typing import List

from apps.game.dto.impact import CalculatedImpact
from apps.game.exceptions import GameLogicException
from apps.game.services.character.core import CharacterService
from apps.school.dto import Impact
from apps.school.models import Skill


class SkillImpactService:
    logger = logging.getLogger("game.services.skill_impact")

    def __init__(self, skill: Skill, character: CharacterService):
        self.initiator = character
        self.skill = skill

    def calculate_impact(self) -> List[CalculatedImpact]:
        self.logger.info(
            f"Calculating impact for skill {self.skill.id} used by character {self.initiator.character.id}")

        if self.skill.type not in (Skill.Types.ATTACK, Skill.Types.HEAL, Skill.Types.SPECIAL):
            self.logger.error("Only attack skills supported for now")
            raise GameLogicException("Only attack skills supported for now")

        impacts: List[Impact] = self.skill.impact
        calculated_impacts = [self.calculate_damage(impact) for impact in impacts]
        if self.skill.type == Skill.Types.HEAL:
            for impact in calculated_impacts:
                impact['value'] *= -1
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
        self.logger.debug(f"Base damage: {base_damage}")
        # FIXME: decide on this
        # if len(required_stats) != len(scaling_factors):
        #     raise GameLogicException("Improperly configured impact formula")

        potential_impacts = []
        for r, s in zip(required_stats, scaling_factors):
            stat_name = r['stat']
            stat_value = self.initiator.get_stat(stat_name)
            required_value = r['value']
            scaling_factor = s['value']
            skill_efficiencies = stat_value / required_value if required_value > 0 else 0.01
            skill_efficiencies *= 1 + (skill_efficiencies - 1) * scaling_factor
            logging.debug(f"Calculating impact based on stat {r['stat']} Skill efficiencies: {skill_efficiencies}, "
                          f"scaling factor: {scaling_factor}, resulting value: {skill_efficiencies}")
            potential_impacts.append(skill_efficiencies)
        final_impact = base_damage * min(potential_impacts or [1])
        logging.debug(f"Final impact: {final_impact}")
        return CalculatedImpact(kind=impact['kind'], value=final_impact)
