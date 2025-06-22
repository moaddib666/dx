import logging
import math
from threading import Lock
from typing import List, Dict, Optional

from apps.school.dto import Impact
from apps.school.models import Skill


class SkillPowerCache:
    """
    Thread-safe singleton cache for skill power ratings.
    """
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._cache = {}
                    cls._instance._breakdown_cache = {}
                    cls._instance._cache_lock = Lock()
        return cls._instance

    def get_power(self, skill_id: int) -> Optional[float]:
        """Get cached power rating for a skill."""
        with self._cache_lock:
            return self._cache.get(skill_id)

    def set_power(self, skill_id: int, power: float) -> None:
        """Cache power rating for a skill."""
        with self._cache_lock:
            self._cache[skill_id] = power

    def get_breakdown(self, skill_id: int) -> Optional[dict]:
        """Get cached power breakdown for a skill."""
        with self._cache_lock:
            return self._breakdown_cache.get(skill_id)

    def set_breakdown(self, skill_id: int, breakdown: dict) -> None:
        """Cache power breakdown for a skill."""
        with self._cache_lock:
            self._breakdown_cache[skill_id] = breakdown

    def invalidate_skill(self, skill_id: int) -> None:
        """Remove a specific skill from cache."""
        with self._cache_lock:
            self._cache.pop(skill_id, None)
            self._breakdown_cache.pop(skill_id, None)

    def clear_cache(self) -> None:
        """Clear all cached data."""
        with self._cache_lock:
            self._cache.clear()
            self._breakdown_cache.clear()

    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        with self._cache_lock:
            return {
                'power_cache_size': len(self._cache),
                'breakdown_cache_size': len(self._breakdown_cache),
                'cached_skills': list(self._cache.keys())
            }


class SkillPowerService:
    """
    Service for calculating skill power rating for sorting and comparison purposes.
    This is a fast calculation that doesn't require character stats.
    """
    logger = logging.getLogger("game.services.skill_power")

    def __init__(self, skill: Skill, use_cache: bool = True):
        self.skill = skill
        self.use_cache = use_cache
        self.cache = SkillPowerCache() if use_cache else None

    def calculate_power_rating(self, force_recalculate: bool = False) -> float:
        """
        Calculates a power rating for the skill based on its inherent properties.
        Uses cache by default unless force_recalculate is True.

        :param force_recalculate: If True, bypasses cache and recalculates.
        :return: A numeric power rating that can be used for sorting skills.
        """
        # Check cache first (unless forced to recalculate or cache disabled)
        if not force_recalculate and self.use_cache and self.cache:
            cached_power = self.cache.get_power(self.skill.id)
            if cached_power is not None:
                self.logger.debug(f"Using cached power rating for skill {self.skill.id}: {cached_power}")
                return cached_power

        self.logger.debug(f"Calculating power rating for skill {self.skill.id}")

        impacts: List[Impact] = self.skill.impact

        if not impacts:
            power_rating = 0.0
        else:
            # Calculate base power from all impacts
            total_base_power = sum(self._calculate_impact_power(impact) for impact in impacts)

            # Apply efficiency modifiers based on resource costs
            power_rating = self._apply_efficiency_modifiers(total_base_power)

        # Cache the result
        if self.use_cache and self.cache:
            self.cache.set_power(self.skill.id, power_rating)

        self.logger.debug(f"Skill {self.skill.id} power rating: {power_rating}")
        return power_rating

    def _calculate_impact_power(self, impact: Impact) -> float:
        """
        Calculates the power contribution of a single impact.

        :param impact: The impact to evaluate.
        :return: Power value for this impact.
        """
        formula = impact['formula']
        base_damage = formula.get("base", 0)
        scaling_factors = formula.get("scaling", [])
        required_stats = formula.get("requires", [])
        max_efficiency = formula.get("max_efficiency", 3)

        # Base power from damage
        base_power = base_damage

        # Calculate scaling potential
        scaling_potential = self._calculate_scaling_potential(scaling_factors, required_stats, max_efficiency)

        # Combine base power with scaling potential
        total_impact_power = base_power * (1 + scaling_potential)

        self.logger.debug(f"Impact {impact['kind']} - Base: {base_damage}, "
                          f"Scaling potential: {scaling_potential:.2f}, "
                          f"Total power: {total_impact_power:.2f}")

        return total_impact_power

    def _calculate_scaling_potential(self, scaling_factors: List, required_stats: List, max_efficiency: float) -> float:
        """
        Calculates the theoretical maximum scaling potential of the skill.

        :param scaling_factors: List of scaling factor configurations.
        :param required_stats: List of required stat configurations.
        :param max_efficiency: Maximum efficiency multiplier.
        :return: Scaling potential multiplier.
        """
        if not scaling_factors or not required_stats:
            return 0.0

        # Calculate average scaling factor
        avg_scaling_factor = sum(s.get('value', 0) for s in scaling_factors) / len(scaling_factors)

        # Estimate potential based on maximum efficiency and scaling
        # Assuming optimal stat distribution, the efficiency approaches max_efficiency
        potential_multiplier = (max_efficiency - 1) * (1 + avg_scaling_factor)

        return min(potential_multiplier, 2.0)  # Cap to prevent extreme values

    def _apply_efficiency_modifiers(self, base_power: float) -> float:
        """
        Applies efficiency modifiers based on resource costs.

        :param base_power: The base power before efficiency modifiers.
        :return: Modified power rating.
        """
        # Get resource costs from skill
        energy_cost = getattr(self.skill, 'energy_cost', 1)
        action_points_cost = getattr(self.skill, 'action_points_cost', 1)

        # Avoid division by zero
        energy_cost = max(energy_cost, 1)
        action_points_cost = max(action_points_cost, 1)

        # Calculate efficiency ratios
        energy_efficiency = base_power / energy_cost
        action_efficiency = base_power / action_points_cost

        # Use geometric mean for balanced efficiency consideration
        combined_efficiency = math.sqrt(energy_efficiency * action_efficiency)

        self.logger.debug(f"Energy efficiency: {energy_efficiency:.2f}, "
                          f"Action efficiency: {action_efficiency:.2f}, "
                          f"Combined: {combined_efficiency:.2f}")

        return combined_efficiency

    def get_power_breakdown(self, force_recalculate: bool = False) -> dict:
        """
        Returns a detailed breakdown of how the power rating was calculated.
        Uses cache by default unless force_recalculate is True.

        :param force_recalculate: If True, bypasses cache and recalculates.
        :return: Dictionary with power calculation details.
        """
        # Check cache first (unless forced to recalculate or cache disabled)
        if not force_recalculate and self.use_cache and self.cache:
            cached_breakdown = self.cache.get_breakdown(self.skill.id)
            if cached_breakdown is not None:
                self.logger.debug(f"Using cached breakdown for skill {self.skill.id}")
                return cached_breakdown

        impacts: List[Impact] = self.skill.impact

        breakdown = {
            'skill_id': self.skill.id,
            'total_power': self.calculate_power_rating(force_recalculate),
            'impacts': [],
            'resource_costs': {
                'energy_cost': getattr(self.skill, 'energy_cost', 1),
                'action_points_cost': getattr(self.skill, 'action_points_cost', 1)
            }
        }

        for impact in impacts:
            impact_power = self._calculate_impact_power(impact)
            formula = impact['formula']

            impact_details = {
                'kind': impact['kind'],
                'type': impact['type'],
                'base_damage': formula.get("base", 0),
                'scaling_factors': formula.get("scaling", []),
                'required_stats': formula.get("requires", []),
                'calculated_power': impact_power
            }
            breakdown['impacts'].append(impact_details)

        # Cache the result
        if self.use_cache and self.cache:
            self.cache.set_breakdown(self.skill.id, breakdown)

        return breakdown

    def invalidate_cache(self) -> None:
        """
        Invalidates cache for this specific skill.
        Useful when skill properties have been modified.
        """
        if self.use_cache and self.cache:
            self.cache.invalidate_skill(self.skill.id)
            self.logger.info(f"Cache invalidated for skill {self.skill.id}")

    @classmethod
    def clear_all_cache(cls) -> None:
        """
        Clears all cached power calculations.
        Useful for memory management or when many skills have been modified.
        """
        cache = SkillPowerCache()
        cache.clear_cache()
        cls.logger.info("All skill power cache cleared")

    @classmethod
    def get_cache_statistics(cls) -> dict:
        """
        Returns cache usage statistics.
        """
        cache = SkillPowerCache()
        return cache.get_cache_stats()


class SkillPowerComparer:
    """
    Utility class for comparing and sorting skills by power with caching support.
    """

    @staticmethod
    def sort_skills_by_power(skills: List[Skill], reverse: bool = True, use_cache: bool = True) -> List[Skill]:
        """
        Sorts a list of skills by their power rating.

        :param skills: List of skills to sort.
        :param reverse: If True, sorts from highest to lowest power.
        :param use_cache: If True, uses cached power calculations.
        :return: Sorted list of skills.
        """

        def get_power(skill):
            service = SkillPowerService(skill, use_cache=use_cache)
            return service.calculate_power_rating()

        return sorted(skills, key=get_power, reverse=reverse)

    @staticmethod
    def get_power_rankings(skills: List[Skill], use_cache: bool = True) -> List[dict]:
        """
        Returns a list of skills with their power ratings for comparison.

        :param skills: List of skills to rank.
        :param use_cache: If True, uses cached power calculations.
        :return: List of dictionaries with skill and power information.
        """
        rankings = []

        for skill in skills:
            service = SkillPowerService(skill, use_cache=use_cache)
            power = service.calculate_power_rating()

            rankings.append({
                'skill': skill,
                'power_rating': power,
                'skill_id': skill.id,
                'name': getattr(skill, 'name', f'Skill {skill.id}')
            })

        # Sort by power rating (highest first)
        rankings.sort(key=lambda x: x['power_rating'], reverse=True)

        # Add rank numbers
        for i, ranking in enumerate(rankings, 1):
            ranking['rank'] = i

        return rankings

    @staticmethod
    def batch_calculate_powers(skills: List[Skill], use_cache: bool = True,
                               force_recalculate: bool = False) -> Dict[int, float]:
        """
        Efficiently calculates power ratings for multiple skills.

        :param skills: List of skills to calculate power for.
        :param use_cache: If True, uses cached power calculations.
        :param force_recalculate: If True, forces recalculation even if cached.
        :return: Dictionary mapping skill_id to power_rating.
        """
        power_ratings = {}

        for skill in skills:
            service = SkillPowerService(skill, use_cache=use_cache)
            power = service.calculate_power_rating(force_recalculate=force_recalculate)
            power_ratings[skill.id] = power

        return power_ratings

    @staticmethod
    def preload_cache(skills: List[Skill]) -> None:
        """
        Preloads the cache with power calculations for a list of skills.
        Useful for warming up the cache during application startup.

        :param skills: List of skills to preload.
        """
        logger = logging.getLogger("game.services.skill_power")
        logger.info(f"Preloading cache for {len(skills)} skills")

        for skill in skills:
            service = SkillPowerService(skill, use_cache=True)
            service.calculate_power_rating()

        logger.info("Cache preloading completed")

    @staticmethod
    def invalidate_skills_cache(skill_ids: List[int]) -> None:
        """
        Invalidates cache for multiple skills.

        :param skill_ids: List of skill IDs to invalidate.
        """
        cache = SkillPowerCache()
        for skill_id in skill_ids:
            cache.invalidate_skill(skill_id)


# Convenience functions for common operations
def get_skill_power(skill: Skill, use_cache: bool = True) -> float:
    """
    Quick function to get a skill's power rating.

    :param skill: The skill to evaluate.
    :param use_cache: Whether to use cached results.
    :return: Power rating.
    """
    service = SkillPowerService(skill, use_cache=use_cache)
    return service.calculate_power_rating()


def get_top_skills(skills: List[Skill], limit: int = 10, use_cache: bool = True) -> List[Skill]:
    """
    Get the top N most powerful skills.

    :param skills: List of skills to evaluate.
    :param limit: Maximum number of skills to return.
    :param use_cache: Whether to use cached results.
    :return: List of top skills sorted by power.
    """
    sorted_skills = SkillPowerComparer.sort_skills_by_power(skills, use_cache=use_cache)
    return sorted_skills[:limit]


def clear_skill_cache():
    """
    Convenience function to clear all skill power cache.
    """
    SkillPowerService.clear_all_cache()
