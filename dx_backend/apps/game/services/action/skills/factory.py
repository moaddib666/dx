from apps.core.models import SpecialSkillType
from apps.game.exceptions import GameException
from .action_skill_default import NoActionSkill
from .proto import SpecialSkillActionFactoryPrototype, SpecialSkillActionPrototype


class SpecialActionFactory(SpecialSkillActionFactoryPrototype):
    __mapping__: dict[SpecialSkillType, SpecialSkillActionPrototype] = {
        SpecialSkillType.REGULAR_ACTION: NoActionSkill,
    }

    def create(self, skill) -> SpecialSkillActionPrototype:
        """
        Creates a SpecialSkillAction instance based on the provided skill.
        """
        if skill.special in self.__mapping__:
            return self.__mapping__[skill.special](skill)
        else:
            raise GameException(f"Unsupported special skill type: {skill.special}")
