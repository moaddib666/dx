from .proto import SpecialSkillActionPrototype
from ...character.character_base_stats import CharacterBaseStatsService
from ...rand_dice import DiceService


class ResetStatsActionSkill(SpecialSkillActionPrototype):
    """
    Represents a no-action skill in the game.
    This class is used when no specific action is required.
    """

    def perform(self, action, calculated_impacts=None, dice_result=None, multiplier=None) -> list:
        """
        Executes the no-action skill. Returns an empty list as no impacts are calculated.

        Args:
            action: The character action being performed
            calculated_impacts: List of calculated impacts for the action
            dice_result: The result of the dice roll
            multiplier: The multiplier for the action
        """
        CharacterBaseStatsService(action.initiator, DiceService).reset_base_stats()
        action.save()
        action.initiator.resetting_base_stats = True
        action.initiator.save(update_fields=["resetting_base_stats"])
        return []
