from apps.world.models import Position
from .proto import SpecialSkillActionPrototype


class TeleportToSafeZoneSkill(SpecialSkillActionPrototype):
    """
    Represents a teleport to safe zone skill in the game.
    This skill teleports the character to their last safe position or a default safe position.
    """

    def perform(self, action, calculated_impacts=None, dice_result=None, multiplier=None) -> list:
        """
        Teleports the character to their last safe position or a default safe position.
        Returns the calculated impacts.

        Args:
            action: The character action being performed
            calculated_impacts: List of calculated impacts for the action
            dice_result: The result of the dice roll
            multiplier: The multiplier for the action
        """
        # Teleport to safe place
        action.initiator.position = action.initiator.last_safe_position or Position.objects.get(
            grid_x=0, grid_y=1, grid_z=1,
        )
        action.initiator.save(
            update_fields=["position", "updated_at"]
        )

        return calculated_impacts or []
