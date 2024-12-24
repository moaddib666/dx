from apps.game.exceptions import GameLogicException
from apps.game.services.action.base_service import BaseService


class DimensionActionService(BaseService):
    def run(self):
        pass

    def check(self):
        if self.action.action_type != self.action.ActionType.DIMENSION_SHIFT:
            raise GameLogicException("Invalid action type")

        if self.action.target_dimension is None:
            raise GameLogicException("No target dimension")

        if self.action.target_dimension.grade > self.initiator.character.rank.grade:
            raise GameLogicException("Invalid target dimension grade")

        if self.initiator.character.dimension_id == self.action.target_dimension:
            raise GameLogicException("Already in target dimension")

        if abs(self.initiator.character.dimension_id - self.action.target_dimension_id) > 1:
            raise GameLogicException("Invalid target dimension")

        if self.action.target_dimension_id > self.initiator.character.dimension_id and self.initiator.character.current_energy_points < 10:
            raise GameLogicException(
                f"Not enough energy current: {self.initiator.character.current_energy_points}, expected: 10")

        if self.initiator.character.current_active_points < self.initiator.get_max_ap():
            raise GameLogicException(f"Not enough action points {self.initiator.character.current_active_points} expected: {self.initiator.get_max_ap()}")

        self.initiator.character.current_active_points = 0
        self.initiator.character.save()
