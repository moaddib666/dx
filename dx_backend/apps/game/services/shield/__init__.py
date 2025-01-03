from apps.action.models import DiceRollResult
from apps.core.models import GameObject
from apps.game.dto.impact import CalculatedImpact
from apps.shields.models import ActiveShield


class ActiveShieldLifeCycleService:

    def __init__(self, shields: [ActiveShield]):
        self.active_shields = shields

    def decrease_cycles(self):
        for shield in self.active_shields:
            shield.cycles_left -= 1
            shield.save()
            if shield.cycles_left <= 0:
                shield.delete()


class ShieldAssessmentService:

    def __init__(self, target: GameObject):
        self.target = target

    def assign_shield(self, calculated_impact: CalculatedImpact, dice_result: DiceRollResult):
        self.target.shields.update_or_create(
            shield_id=calculated_impact.get('violation'),
            defaults={
                'health': calculated_impact.get('value', 15),
                'cycles_left': min(dice_result.dice_side, 5)
            }
        )


class ActiveShieldImpactService:

    def __init__(self, shields: [ActiveShield]):
        self.map = {
            shield.shield.id: shield for shield in shields
        }

    def apply_impact(self, impact: CalculatedImpact) -> CalculatedImpact:
        shield = self.map.get(impact.get('violation'))
        if not shield:
            return impact
        # shield efficiency is a float between 0 and 1 where 1 is 100% efficiency no damage to player
        damage_to_player = impact['value'] * (1 - shield.efficiency)
        damage_to_shield = impact['value'] - damage_to_player
        impact['value'] = damage_to_player + self.impact_shield(shield, damage_to_shield)
        return impact

    def impact_shield(self, shield: ActiveShield, value: int) -> int:
        shield.health -= value

        if shield.health < 0:
            shield.delete()
            self.map.pop(shield.shield.id)
            return abs(shield.health)
        shield.save(
            update_fields=['health', 'updated_at']
        )
        return 0
