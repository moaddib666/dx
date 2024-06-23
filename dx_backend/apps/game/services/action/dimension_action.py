from apps.game.exceptions import GameLogicException
from apps.game.services.action.base_service import BaseService


class DimensionActionService(BaseService):
    def run(self):
        pass

    def check(self):
        if self.action.action_type != self.action.ActionType.dimension_shift:
            raise GameLogicException("Invalid action type")

        if self.action.target_dimension is None:
            raise GameLogicException("No target dimension")

        if self.initiator.player.dimension_id == self.action.target_dimension:
            raise GameLogicException("Already in target dimension")

        if abs(self.initiator.player.dimension_id - self.action.target_dimension_id) > 1:
            raise GameLogicException("Invalid target dimension")

        if self.action.target_dimension_id > self.initiator.player.dimension_id and self.initiator.player.current_energy_points < 10:
            raise GameLogicException("Not enough energy")

        if self.initiator.player.current_active_points < self.initiator.get_max_ap():
            raise GameLogicException("Not enough energy")

        self.initiator.player.current_active_points = 0
        self.initiator.player.save()


