import math

import typing as t

if t.TYPE_CHECKING:
    from apps.core.models import CharacterStats
    from apps.school.dto import Formula
    from apps.game.services.character.core import CharacterService


class FormulaService:

    def __init__(self, char: "CharacterService", formula: "Formula", use_real_stats: bool = False):
        self.char = char
        self.formula = formula
        self.use_real_stats = use_real_stats

    def get_character_stat(self, stat_name: "CharacterStats") -> int:
        if self.use_real_stats:
            return self.char.get_real_stat(stat_name)
        return self.char.get_stat(stat_name)

    def evaluate(self) -> float:
        """
        Evaluates the formula and returns the final impact.
        """
        base = self.formula.get("base", 1)
        min_efficiency = self.formula.get("min_efficiency", 0.01)
        max_efficiency = self.formula.get("max_efficiency", 3)
        required_stats = self.formula.get("requires", [])
        scaling_factors = self.formula.get("scaling", [])

        potential_impacts = []
        for r, s in zip(required_stats, scaling_factors):
            stat_name = r['stat']
            stat_value = self.get_character_stat(stat_name)
            required_value = r['value']
            scaling_factor = s['value']

            efficiency = self.calculate_efficiency(
                stat_value,
                required_value,
                scaling_factor,
                max_efficiency,
                min_efficiency
            )
            potential_impacts.append(efficiency)

        final_impact = base * min(potential_impacts or [1])
        return final_impact

    @staticmethod
    def calculate_efficiency(stat_value: int, required_value: int, scaling_factor: float,
                             max_efficiency: float = 3, min_efficiency: float = 0.01) -> float:
        """
        Calculates the efficiency of a stat based on a required value and a scaling factor.
        """
        if required_value > 0:
            ratio = stat_value / required_value
            normalized_log = math.log10(1 + ratio) / math.log10(2)
            base_efficiency = 1
            efficiency = base_efficiency + (normalized_log - base_efficiency) * (1 + scaling_factor)
        else:
            efficiency = min_efficiency * (1 + scaling_factor)

        return max(min(max_efficiency, efficiency), min_efficiency)

    def evaluate_int(self) -> int:
        value = self.evaluate()
        if value - int(value) == 0.5:
            return int(value)  # Round down for .5
        else:
            return int(value) + 1  # Round up for all other cases
