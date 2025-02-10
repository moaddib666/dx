import abc
import logging
import typing as t

from apps.action.models import CharacterAction, DiceRollResult
from apps.character.models import Character
from apps.core.models import CharacterStats, SkillTypes
from apps.game.dto.impact import CalculatedImpact
from apps.game.exceptions import GameException
from apps.game.services.action.base_service import CharacterActionServicePrototype
from apps.game.services.character.core import CharacterService
from apps.game.services.rand_dice import DiceService
from apps.game.services.shield import ActiveShieldImpactService, ShieldAssessmentService
from apps.game.services.skills.cost_validator import SkillCostService
from apps.game.services.skills.impact_calculator import SkillImpactService
from apps.world.models import Position

if t.TYPE_CHECKING:
    from apps.game.services.effect.assigner import BaseEffectAssigner


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

    def __init__(self, effect_assigner: "BaseEffectAssigner", gm_mode: bool = False, ):
        self.gm_mode = gm_mode
        self.effect_assigner = effect_assigner

    def perform(self, action: CharacterAction):
        initiator = CharacterService(action.initiator)
        calculated_impacts = SkillImpactService(action.skill, initiator).calculate_impact()
        multiplier = DiceService(initiator.model, initiator.get_stat(CharacterStats.LUCK)).multiplier_roll()
        dice_result = DiceRollResult.objects.create(
            dice_side=multiplier.dice_side,
            multiplier=multiplier.multiplier,
            outcome=multiplier.outcome
        )

        if action.skill.type == SkillTypes.SPECIAL:
            self._perform_special(action, calculated_impacts, dice_result, multiplier)
            return

        if action.skill.type == SkillTypes.HEAL:
            self._perform_heal(action, calculated_impacts, dice_result, multiplier)
            return

        if action.skill.type == SkillTypes.ATTACK:
            self._perform_damage(action, calculated_impacts, dice_result, multiplier)
            return

        if action.skill.type == SkillTypes.DEFENSE:
            self._perform_defense(action, calculated_impacts, dice_result, multiplier)
            return

        if action.skill.type == SkillTypes.BUFF:
            self._assign_effect(action, calculated_impacts, dice_result, multiplier)
            return

        raise GameException("Skill type not implemented")

    def check(self, action: CharacterAction):
        pass

    def _assign_effect(self, action, calculated_impacts, dice_result, multiplier):
        for target in action.targets.filter(is_active=True):
            if action.skill.effect:
                if isinstance(action.skill.effect, list):
                    for effect in action.skill.effect:
                        self.effect_assigner.assign_effect(effect, CharacterService(target), CharacterService(action.initiator))
                    return
                self.effect_assigner.assign_effect(action.skill.effect, CharacterService(target), CharacterService(action.initiator))

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

    # TODO: refactor this to use performers instead
    def _perform_special(self, action, calculated_impacts, dice_result, multiplier):
        if dice_result.outcome == 1:
            self.logger.debug(
                f"Special action failed for action {action.id} in cycle {action.cycle_id} due to dice roll")
            return

        if action.skill_id == 168:  # case 1: teleport to safe place
            # TODO: use location service for this
            action.initiator.position = action.initiator.last_safe_position or Position.objects.get(
                grid_x=0, grid_y=1, grid_z=1,
            )
            action.initiator.save(
                update_fields=["position", "updated_at"]
            )
            for impact in calculated_impacts:
                self._register_impact(action, action.initiator, impact, dice_result)
            return
        if action.skill_id == 167:  # case 2: accumulate energy
            char_svc = CharacterService(action.initiator)
            calculate_amount = (char_svc.get_max_energy() * 0.7) * multiplier.multiplier
            char_svc.add_energy(calculate_amount)
            for impact in calculated_impacts:
                impact['value'] = calculate_amount
                self._register_impact(action, action.initiator, impact, dice_result)
            return
        raise GameException("Special action not implemented")

    def _perform_heal(self, action, calculated_impacts, dice_result, multiplier):
        # TODO: refactor this to use performers instead and give up hack w
        for impact in calculated_impacts:
            impact['value'] *= -1
        self._perform_damage(action, calculated_impacts, dice_result, multiplier)

    def _perform_damage(self, action, calculated_impacts, dice_result, multiplier):
        for calculated_impact in calculated_impacts:
            calculated_impact['value'] = int(calculated_impact['value'] * multiplier.multiplier)
            self.logger.debug(
                f"Calculated impact damage {calculated_impact['value']} for action {action.id} in cycle {action.cycle_id}")
            for target in action.targets.filter(is_active=True):
                target_character = CharacterService(target)
                shields_service = ActiveShieldImpactService(target_character.get_shields())
                calculated_impact = shields_service.apply_impact(calculated_impact)
                target_character.impacted(action, calculated_impact, dice_result)
                rs = [self._register_impact(action, target, calculated_impact, dice_result), ]
                self.logger.debug(
                    f"Applied impact to target character {target.id} from action {action.id} in cycle {action.cycle_id}",
                    extra={
                        "impacts": rs
                    })

    def _perform_defense(self, action, calculated_impacts, dice_result, multiplier):
        for calculated_impact in calculated_impacts:
            calculated_impact['value'] = int(calculated_impact['value'] * multiplier.multiplier)
            self.logger.debug(
                f"Calculated impact deface {calculated_impact['value']} for action {action.id} in cycle {action.cycle_id}")
            for target in action.targets.filter(is_active=True):
                shields_service = ShieldAssessmentService(target)
                shields_service.assign_shield(calculated_impact, dice_result)
                rs = [self._register_impact(action, target, calculated_impact, dice_result), ]
                self.logger.debug(
                    f"Applied shield to target character {target.id} from action {action.id} in cycle {action.cycle_id}",
                    extra={
                        "impacts": rs
                    })

    def _register_impact(self, action, target: Character, calculated_impact: CalculatedImpact,
                         dice_roll_result: DiceRollResult):
        action.impacts.create(
            target=target,
            type=calculated_impact["kind"],
            violation=calculated_impact["violation"],
            size=calculated_impact['value'],
            dice_roll_result=dice_roll_result
        )
