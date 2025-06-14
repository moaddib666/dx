from apps.game.services.character.core import CharacterService
from .proto import SpecialSkillActionPrototype


class FlowAccumulationSkill(SpecialSkillActionPrototype):
    """
    Represents a flow accumulation skill in the game.
    This skill increases the character's energy.
    """

    def perform(self, action, calculated_impacts=None, dice_result=None, multiplier=None) -> list:
        """
        Increases the character's energy.
        Returns the calculated impacts with updated values.
        
        Args:
            action: The character action being performed
            calculated_impacts: List of calculated impacts for the action
            dice_result: The result of the dice roll
            multiplier: The multiplier for the action
        """
        if not calculated_impacts:
            calculated_impacts = []

        char_svc = CharacterService(action.initiator)
        calculate_amount = (char_svc.get_max_energy() * 0.7) * multiplier.multiplier
        char_svc.add_energy(calculate_amount)

        # Update impact values
        for impact in calculated_impacts:
            impact['value'] = calculate_amount

        return calculated_impacts
