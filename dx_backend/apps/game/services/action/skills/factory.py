from apps.core.models import SpecialSkillType
from apps.game.exceptions import GameException
from .action_skill_default import NoActionSkill
from .action_skill_flow_accumulation import FlowAccumulationSkill
from .action_skill_reset_stats import ResetStatsActionSkill
from .action_skill_teleport import TeleportToSafeZoneSkill
from .proto import SpecialSkillActionFactoryPrototype, SpecialSkillActionPrototype


class SpecialActionFactory(SpecialSkillActionFactoryPrototype):
    __mapping__: dict[SpecialSkillType, SpecialSkillActionPrototype] = {
        SpecialSkillType.REGULAR_ACTION: NoActionSkill,
        SpecialSkillType.TELEPORT_TO_SAFE_ZONE: TeleportToSafeZoneSkill,
        SpecialSkillType.FLOW_ACCUMULATION: FlowAccumulationSkill,
        SpecialSkillType.RESET_STATS: ResetStatsActionSkill,
    }

    def create(self, skill) -> SpecialSkillActionPrototype:
        """
        Creates a SpecialSkillAction instance based on the provided skill.
        """

        if skill.special in self.__mapping__:
            return self.__mapping__[skill.special](skill)

        # Backward compatibility for old skills
        if skill.id == 168:
            return TeleportToSafeZoneSkill(skill)
        if skill.id == 167:
            return FlowAccumulationSkill(skill)

        raise GameException(f"Unsupported special skill type: {skill.special}")
