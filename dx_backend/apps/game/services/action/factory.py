from apps.core.models import PlayerActionType
from apps.fight.models import FightTurnAction
from apps.game.services.action.dimension_action import DimensionActionService
from apps.game.services.action.skill_action import SkillActionService
from apps.game.services.player.core import PlayerService


class ActionFactory:
    pass


class FightActionFactory:

    mapping = {
        PlayerActionType.USE_SKILL: SkillActionService,
        PlayerActionType.DIMENSION_SHIFT: DimensionActionService,
    }

    def from_action(self, action: FightTurnAction):
        initiator = PlayerService(action.initiator)
        targets = [PlayerService(target) for target in action.targets.all()]
        return self.mapping[action.action_type](action, initiator, targets)
