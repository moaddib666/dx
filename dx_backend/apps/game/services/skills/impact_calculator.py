import logging
import math
from typing import List

from apps.game.dto.impact import CalculatedImpact
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

        impacts: List[Impact] = self.skill.impact
        calculated_impacts = [self.calculate_damage(impact) for impact in impacts]
        return calculated_impacts

    def calculate_damage(self, impact: Impact) -> CalculatedImpact:
        """
        Calculates the damage for a given impact based on a formula that includes base damage, required stats,
        and scaling factors. The scaling factor calculation now uses the logarithm base 10 of the stat ratio,
        multiplied by (1 + scaling factor).

        :param impact: Impact data containing the damage formula and kind.
        :return: A CalculatedImpact instance with the final damage value and violation type.
        """
        self.logger.info(f"Calculating damage for impact {impact['kind']}")

        # Extract the formula details from the impact
        formula = impact['formula']
        base_damage = formula.get("base", 0)  # Base damage value
        required_stats = formula.get("requires", [])  # List of required stats with their minimum values
        scaling_factors = formula.get("scaling", [])  # List of scaling factors for each stat

        self.logger.debug(f"Base damage: {base_damage}")

        potential_impacts = []

        # Iterate through required stats and their corresponding scaling factors
        for r, s in zip(required_stats, scaling_factors):
            stat_name = r['stat']  # Name of the stat to consider
            stat_value = self.initiator.get_stat(stat_name)  # Get the initiator's stat value
            required_value = r['value']  # Required minimum value for the stat
            scaling_factor = s['value']  # Scaling factor for this stat

            # Calculate the efficiency of the stat based on logarithm base 10
            if required_value > 0:
                # skill_efficiency = math.log10(max(stat_value / required_value, 0.01)) * (1 + scaling_factor)
                # FIXME: required_value now not used
                skill_efficiency = math.log10(stat_value) * (1 + scaling_factor)
            else:
                skill_efficiency = 0.01 * (1 + scaling_factor)  # Avoid divide-by-zero errors

            self.logger.debug(f"Calculating impact based on stat {r['stat']}. Skill efficiency: {skill_efficiency}, "
                              f"scaling factor: {scaling_factor}, resulting value: {skill_efficiency}")
            potential_impacts.append(skill_efficiency)

        # Final impact is base damage scaled by the minimum skill efficiency
        final_impact = base_damage * max(potential_impacts or [1])
        self.logger.debug(f"Final impact: {final_impact}")

        # Return the calculated impact as an instance of CalculatedImpact
        return CalculatedImpact(kind=impact['kind'], value=int(final_impact), violation=impact['type'])
