import typing as t

from apps.core.models import GodIntervention, AttributeType, ImpactType, ImpactViolationType, ActionImpactModel
from apps.game.services.character.core import CharacterService


class GodInterventionService:
    """
    Service for applying blessings to characters.
    """

    def __init__(self, target_character: CharacterService):
        """
        Initialize the god_intervention_service service with a target character.

        Args:
            target_character: The character service instance for the target character
        """
        self.target_character = target_character

    def act(self, intervention: GodIntervention) -> t.List[ActionImpactModel]:
        """
        Apply a god_intervention_service to the target character.

        Args:
            intervention: The god_intervention_service to apply

        Returns:
            List of action impacts resulting from the god_intervention_service
        """
        # Roll dice to determine the effectiveness of the god_intervention_service
        dice_svc = self.target_character.get_dice_service()(
            sides=20
        )
        dice_roll_result = dice_svc.multiplier_roll()

        # Apply immediate impacts based on the god_intervention_service
        impacts = []
        for attribute in intervention.attributes:
            impact = self._apply_attribute_changes(intervention, dice_roll_result, attribute)
            impacts.append(impact)
        return impacts

    def _apply_attribute_changes(self, intervention: GodIntervention, dice_roll_result,
                                 attribute: AttributeType) -> ActionImpactModel:
        base_persent = intervention.size.float_value()
        max_attribute = self.target_character.get_max_attribute(attribute)
        multiplier = dice_roll_result.multiplier
        change_size = int(max_attribute * base_persent * multiplier)

        if intervention.type.is_curse():
            self.target_character.spend_attribute(attribute, change_size)
        else:
            self.target_character.increase_attribute(attribute, change_size)
        return ActionImpactModel(
            type=ImpactType.NONE,
            violation=ImpactViolationType.NONE,
            size=change_size,
            dice_roll_result=dice_roll_result
        )
