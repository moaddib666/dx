import abc
import logging

from apps.action.models import CharacterAction, DiceRollResult
from apps.core.models import CharacterStats
from apps.game.exceptions import GameException
from apps.game.services.action.base_service import CharacterActionServicePrototype
from apps.game.services.character.core import CharacterService
from apps.game.services.rand_dice import DiceService
from apps.game.services.skills.cost_validator import SkillCostService
from apps.game.services.skills.impact_calculator import SkillImpactService


class AbstractImpactActionApplicator(abc.ABC):

    def __init__(self, action: CharacterAction, char: CharacterService):
        self.action = action
        self.char = char

    @abc.abstractmethod
    def is_applicable(self) -> bool:
        """Should return True if the action is applicable and need further checks"""
        pass

    @abc.abstractmethod
    def is_acceptable(self) -> bool:
        """
        Should return True if the action is acceptable and can be performed
        """
        pass

    @abc.abstractmethod
    def accept(self):
        """
        Prepare remove action points and perform the other preparation steps
        """
        pass


class PhysicalImpactActionApplicator(AbstractImpactActionApplicator):

    def is_applicable(self) -> bool:
        pass

    def is_acceptable(self) -> bool:
        pass

    def accept(self):
        pass


class ImpactAction(CharacterActionServicePrototype):
    character_svc_cls = CharacterService
    impact_applicators: list[type[AbstractImpactActionApplicator]] = [
        PhysicalImpactActionApplicator
    ]

    logger = logging.getLogger(__name__)

    def __init__(self, gm_mode: bool = False):
        self.gm_mode = gm_mode

    def perform(self, action: CharacterAction):
        initiator = CharacterService(action.initiator)
        calculated_impacts = SkillImpactService(action.skill, initiator).calculate_impact()
        multiplier = DiceService(initiator.model, initiator.get_stat(CharacterStats.LUCK)).multiplier_roll()
        dice_result = DiceRollResult.objects.create(
            dice_side=multiplier.dice_side,
            multiplier=multiplier.multiplier,
            outcome=multiplier.outcome
        )
        for calculated_impact in calculated_impacts:
            calculated_impact['value'] = int(calculated_impact['value'] * multiplier.multiplier)
            self.logger.debug(
                f"Calculated impact damage {calculated_impact['value']} for action {action.id} in cycle {action.cycle_id}")
            for target in action.targets.all():
                target_character = CharacterService(target)
                rs = target_character.impacted(action, calculated_impact, dice_result)
                self.logger.debug(
                    f"Applied impact to target character {target.id} from action {action.id} in cycle {action.cycle_id}",
                    extra={
                        "impacts": rs
                    })
        action.perform()

    def check(self, action: CharacterAction):
        pass

    def check_acceptance(self, action: CharacterAction):
        """
        The initiator need to have enough action points, energy points and health points to perform the action
        Let's simplify the impact actions
        Damage actions cost 4 action points
        If Magical it cost all action points
        If Magical base damage is 30
        If Physical base damage is 15
        Heal actions cost all action points
        Magical actions cost 10 energy points
        Physical actions cost 3 energy points
        """
        initiator = action.initiator
        svc = self.character_svc_cls(initiator)
        self._check_acceptance(action, svc)

    def _check_acceptance(self, action: CharacterAction, svc: CharacterService):
        for applicator_cls in self.impact_applicators:
            applicator = applicator_cls(action, svc)
            if not applicator.is_applicable():
                continue
            if not applicator.is_acceptable():
                raise GameException("Not enough resources")

    def _accept(self, action: CharacterAction, svc: CharacterService):
        for applicator_cls in self.impact_applicators:
            applicator = applicator_cls(action, svc)
            if not applicator.is_applicable():
                continue
            if not applicator.is_acceptable():
                raise GameException("Not enough resources")
            applicator.accept()

    def accept(self, action: CharacterAction):
        self.check_acceptance(action)
        self._accept(action, self.character_svc_cls(action.initiator))
        SkillCostService(action.skill).apply(action.initiator)
        action.accept()
