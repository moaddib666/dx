from apps.core.models import CharacterActionType
from apps.fight.models import FightTurnAction
from apps.game.services.action.dimension_action import DimensionActionService
from apps.game.services.action.skill_action import SkillActionService
from apps.game.services.character.core import CharacterService


class ActionFactory:
    pass


class FightActionFactory:

    mapping = {
        CharacterActionType.USE_SKILL: SkillActionService,
        CharacterActionType.DIMENSION_SHIFT: DimensionActionService,
    }

    def from_action(self, action: FightTurnAction):
        initiator = CharacterService(action.initiator)
        targets = [CharacterService(target) for target in action.targets.all()]
        return self.mapping[action.action_type](action, initiator, targets)
