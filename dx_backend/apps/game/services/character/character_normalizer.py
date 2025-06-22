import typing as t

from apps.core.models import NormalizedCharacterPower, CharacterStats, TheChosenPath

if t.TYPE_CHECKING:
    from apps.game.services.character.core import CharacterService


class CharacterPowerNormalizer:

    def normalize(self, character_service: "CharacterService") -> NormalizedCharacterPower:
        base = 10 - character_service.rank_grade
        speed = character_service.get_current_speed()

        max_energy = character_service.get_max_energy()
        current_energy = character_service.get_current_energy()

        max_health = character_service.get_max_hp()
        current_health = character_service.get_current_hp()

        path = character_service.get_path()

        stats_power = 0.0
        for normalizer in DEFINED_PATH_POWER_STATS_NORMALIZERS:
            if normalizer.the_path == path:
                stats_power = normalizer.computed_power(character_service)
                break

        # Calculate max_power: character's theoretical maximum power at full health/energy
        max_power = self._calculate_max_power(
            stats_power=stats_power,
            base=base,
            speed=speed,
            max_health=max_health,
            max_energy=max_energy
        )

        # Calculate current_power: character's effective power considering current state
        current_power = self._calculate_current_power(
            max_power=max_power,
            current_health=current_health,
            max_health=max_health,
            current_energy=current_energy,
            max_energy=max_energy
        )

        return NormalizedCharacterPower(
            id=character_service.get_id(),
            max_power=max_power,
            current_power=current_power,
        )

    def _calculate_max_power(self, stats_power: float, base: float, speed: float,
                             max_health: float, max_energy: float) -> float:
        """
        Calculate the character's maximum theoretical power.

        Formula weights:
        - stats_power: 60% (primary contributor from character's path-specific stats)
        - health_factor: 25% (survivability contribution)
        - energy_factor: 10% (ability to use special abilities)
        - speed_factor: 3% (combat agility)
        - base_factor: 2% (rank/level contribution)
        """
        # Normalize factors to reasonable scales
        health_factor = max_health / 100.0  # Assuming health is typically 0-1000+
        energy_factor = max_energy / 100.0  # Assuming energy is typically 0-1000+
        speed_factor = speed / 50.0  # Assuming speed is typically 0-100
        base_factor = base  # Already in reasonable range (0-10)

        max_power = (
                stats_power * 0.60 +
                health_factor * 0.25 +
                energy_factor * 0.10 +
                speed_factor * 0.03 +
                base_factor * 0.02
        )

        return max(max_power, 0.1)  # Ensure minimum power of 0.1

    def _calculate_current_power(self, max_power: float, current_health: float,
                                 max_health: float, current_energy: float,
                                 max_energy: float) -> float:
        """
        Calculate the character's current effective power.

        Factors affecting current power:
        - health_ratio: 70% impact (heavily injured = much less effective)
        - energy_ratio: 30% impact (low energy = reduced ability usage)

        The formula uses progressive scaling:
        - Health below 25%: severe penalty
        - Health 25-50%: moderate penalty
        - Health 50-75%: light penalty
        - Health above 75%: minimal penalty
        """
        # Calculate ratios
        health_ratio = current_health / max_health if max_health > 0 else 0
        energy_ratio = current_energy / max_energy if max_energy > 0 else 0

        # Progressive health scaling (more severe penalties at low health)
        if health_ratio <= 0.25:
            health_modifier = health_ratio * 0.4  # Very severe penalty when critically injured
        elif health_ratio <= 0.50:
            health_modifier = 0.1 + (health_ratio - 0.25) * 1.6  # Moderate penalty
        elif health_ratio <= 0.75:
            health_modifier = 0.5 + (health_ratio - 0.50) * 1.6  # Light penalty
        else:
            health_modifier = 0.9 + (health_ratio - 0.75) * 0.4  # Minimal penalty when healthy

        # Linear energy scaling (less punitive than health)
        energy_modifier = 0.3 + (energy_ratio * 0.7)  # Min 30% effectiveness even at 0 energy

        # Combine modifiers with weights
        overall_modifier = (health_modifier * 0.7) + (energy_modifier * 0.3)

        current_power = max_power * overall_modifier

        return max(current_power, 0.05)  # Ensure minimum current power


_power_normalizer = CharacterPowerNormalizer()


def normalize_character_power(character_service: "CharacterService") -> NormalizedCharacterPower:
    return _power_normalizer.normalize(character_service)


class PathStatsPowerNormalizer:
    stats_multipliers: dict[CharacterStats, float]
    the_path: TheChosenPath

    def __init__(self, the_path: TheChosenPath,
                 stats_multipliers: dict[CharacterStats, float]):
        self.stats_multipliers = stats_multipliers
        self.the_path = the_path

    def computed_power(self, character_service: "CharacterService") -> float:
        return sum(
            character_service.get_stat(stat) * self.stats_multipliers.get(stat, 1.0)
            for stat in CharacterStats
        )


DEFINED_PATH_POWER_STATS_NORMALIZERS = (
    PathStatsPowerNormalizer(
        TheChosenPath.MAGIC_JSON,
        {
            CharacterStats.CONCENTRATION: 1.5,
            CharacterStats.FLOW_MANIPULATION: 1.5,
            CharacterStats.FLOW_CONNECTION: 1.5,
            CharacterStats.SPEED: 1.2,
            CharacterStats.LUCK: 1.2,
            CharacterStats.CHARISMA: 0.2,
            CharacterStats.KNOWLEDGE: 0.2,
        },
    ),
    PathStatsPowerNormalizer(
        TheChosenPath.TECH_JOHN,
        {
            CharacterStats.PHYSICAL_STRENGTH: 1.5,
            CharacterStats.MENTAL_STRENGTH: 1.5,
            CharacterStats.FLOW_RESONANCE: 1.5,
            CharacterStats.SPEED: 1.2,
            CharacterStats.LUCK: 1.2,
            CharacterStats.CHARISMA: 0.2,
            CharacterStats.KNOWLEDGE: 0.2,
        },
    ),
    PathStatsPowerNormalizer(
        TheChosenPath.NOT_CHOSEN,
        {
            CharacterStats.CHARISMA: 0.2,
            CharacterStats.KNOWLEDGE: 0.2,
        },
    ),
)
