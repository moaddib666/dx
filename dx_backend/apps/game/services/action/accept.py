import typing

from apps.core.models import CharacterStats
from apps.game.services.character.core import CharacterService

if typing.TYPE_CHECKING:
    from apps.action.models import CharacterAction
    from apps.game.services.action.factory import CharacterActionFactory


class ActionAcceptor:
    character_svc_cls = CharacterService

    def __init__(self, action: "CharacterAction", factory: "CharacterActionFactory"):
        self.action = action
        self.action_service = factory.from_action(action)

    def accept(self):
        self.action_service.check_acceptance(self.action)
        self.action_service.accept(self.action)
        self.action.accept(
            order=self.calculate_order(),
        )

    def calculate_order(self) -> float:
        """
        Calculates the order index for the action based on the initiator's speed and turn progress.

        :return: A float representing the action order index (lower is better).
        """
        initiator_svc = self.character_svc_cls(self.action.initiator)
        speed = initiator_svc.get_stat(CharacterStats.SPEED)
        max_ap = initiator_svc.get_max_ap()
        current_ap = initiator_svc.get_current_ap()
        return self._calculate_order(speed, max_ap, current_ap)

    def _calculate_order(self, speed: int, max_ap: int, current_ap: int) -> float:
        """
        Calculates the order index for the action based on the initiator's speed and turn progress.

        :return: A float representing the action order index (lower is better).
        """
        # Calculate turn progress factor
        turn_progress_factor = (max_ap - current_ap) / max_ap

        # Calculate action duration factor (based on speed)
        action_duration_factor = 1 / speed if speed > 0 else float('inf')

        # Combine the factors to determine the overall order index
        order_index = turn_progress_factor + action_duration_factor
        return order_index
