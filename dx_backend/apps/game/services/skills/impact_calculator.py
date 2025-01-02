import logging
import math
from typing import List

from apps.core.models import CharacterStats
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
        and scaling factors. The scaling factor calculation now uses a normalized logarithm base 10.

        :param impact: Impact data containing the damage formula and kind.
        :return: A CalculatedImpact instance with the final damage value and violation type.
        """
        self.logger.info(f"Calculating damage for impact {impact['kind']}")

        # Extract the formula details from the impact
        formula = impact['formula']
        min_efficiency = formula.get("min_efficiency", 0.01)  # Minimum efficiency value
        max_efficiency = formula.get("max_efficiency", 3)  # Maximum efficiency value
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

            skill_efficiency = self.calculate_efficiency(stat_name, required_value, scaling_factor, max_efficiency,
                                                         min_efficiency)
            # Calculate the efficiency of the stat based on the normalized logarithm base 10
            # if required_value > 0:
            #     ratio = stat_value / required_value
            #     normalized_log = math.log10(1 + ratio) / math.log10(2)  # Normalize the logarithm
            #     skill_efficiency = normalized_log * (1 + scaling_factor)  # Apply scaling factor
            # else:
            #     skill_efficiency = 0.01 * (1 + scaling_factor)  # Default efficiency for zero required_value

            self.logger.debug(
                f"Calculating impact based on stat {r['stat']} ({stat_value}). Skill efficiency: {skill_efficiency}, "
                f"scaling factor: {scaling_factor}, resulting value: {skill_efficiency}")
            potential_impacts.append(skill_efficiency)

        # Final impact is base damage scaled by the minimum skill efficiency
        final_impact = base_damage * min(potential_impacts or [1])
        self.logger.debug(f"Final impact: {final_impact}")

        # Return the calculated impact as an instance of CalculatedImpact
        return CalculatedImpact(kind=impact['kind'], value=int(final_impact), violation=impact['type'])

    def calculate_efficiency(self, stat_name: CharacterStats, required_value: int, scaling_factor: float,
                             max_efficiency: float = 3, min_efficiency: float = 0.01) -> float:
        """
        Calculates the efficiency of a stat based on a required value and a scaling factor.

        :param stat_name: The name of the stat to consider.
        :param required_value: The minimum value required for the stat.
        :param scaling_factor: The scaling factor for the stat.
        :param max_efficiency: The maximum efficiency value.
        :param min_efficiency: The minimum efficiency value.
        :return: The calculated efficiency value.
        """
        stat_value = self.initiator.get_stat(stat_name)

        if required_value > 0:
            ratio = stat_value / required_value
            normalized_log = math.log10(1 + ratio) / math.log10(2)  # Normalize the logarithm
            base_efficiency = 1  # Ensure base efficiency is always 1
            efficiency = base_efficiency + (normalized_log - base_efficiency) * (1 + scaling_factor)
        else:
            efficiency = min_efficiency * (1 + scaling_factor)

        # Ensure efficiency is within bounds
        return max(min(max_efficiency, efficiency), min_efficiency)