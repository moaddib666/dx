import logging

from django.db import transaction
from django.utils import timezone

from apps.action.models import DiceRollResult
from apps.core.models import CharacterStats, CharacterActionType
from apps.fight.models import FightTurn, FightTurnAction
from apps.game.exceptions import GameLogicException
from apps.game.services.notifier.fight import FightNotifier
from apps.game.services.character.core import CharacterService
from apps.game.services.rand_dice import DiceService
from apps.game.services.skills.cost_validator import SkillCostService
from apps.game.services.skills.impact_calculator import SkillImpactService


class TurnProcessorService:
    logger = logging.getLogger("game.services.turn_processor")
    notifier: FightNotifier

    def __init__(self, turn: FightTurn, notifier: FightNotifier):
        self.turn = turn
        self.notifier = notifier

    def ready_to_processing(self) -> bool:
        time_left = self.turn.created_at + timezone.timedelta(seconds=self.turn.duration) - timezone.now()
        self.logger.debug(f"Time left for turn {self.turn.id}: {time_left.total_seconds()}")
        return int(time_left.total_seconds()) <= 0

    def check(self):
        self.logger.info(f"Checking turn {self.turn.id}")
        if self.turn.is_finished:
            self.logger.error(f"Turn {self.turn.id} is already finished")
            raise GameLogicException("Turn is finished")

    @transaction.atomic
    def prepare(self):
        self.logger.info(f"Preparing actions for turn {self.turn.id}")
        actions = self.turn.actions.all().select_for_update()
        shifts = actions.filter(action_type=FightTurnAction.ActionType.dimension_shift)
        skills = actions.filter(action_type=FightTurnAction.ActionType.use_skill).order_by('initiator')

        time_taken = 0
        character: CharacterService | None = None
        for action in skills:
            skill = action.skill
            skill_require_ap = SkillCostService(skill).get_ap_cost()
            if not character or character.character.pk != action.initiator_id:
                character = CharacterService(action.initiator)
                time_taken = 0
            time_taken += skill_require_ap * 100 / character.get_current_speed()
            action.order = time_taken
            action.save()
            self.logger.debug(f"Set order {action.order} for action {action.id} in turn {self.turn.id}")
        shifts.update(order=100_000)
        self.logger.info(f"Updated dimension shift actions for turn {self.turn.id}")

    @transaction.atomic
    def play(self):
        self.logger.info(f"Playing actions for turn {self.turn.id}")
        actions = self.turn.actions.all().select_for_update()
        for action in actions:
            initiator = CharacterService(action.initiator)
            if action.action_type == CharacterActionType.DIMENSION_SHIFT:
                r = initiator.dimension_shift(action)
                self.logger.debug(f"Processed dimension shift action {action.id} for turn {self.turn.id}")
                self.notifier.send_action_result(action, [r])
                continue
            if action.action_type == CharacterActionType.USE_SKILL:
                # TODO: refactor this so that calculated impact receive character
                calculated_impacts = SkillImpactService(action.skill, initiator).calculate_impact()
                multiplier = DiceService(initiator.character, initiator.get_stat(CharacterStats.LUCK)).multiplier_roll()
                dice_result = DiceRollResult.objects.create(
                    dice_side=multiplier.dice_side,
                    multiplier=multiplier.multiplier,
                    outcome=multiplier.outcome
                )
                for calculated_impact in calculated_impacts:
                    calculated_impact['value'] = int(calculated_impact['value'] * multiplier.multiplier)
                    self.logger.debug(
                        f"Calculated impact damage {calculated_impact['value']} for action {action.id} in turn {self.turn.id}")
                    for target in action.targets.all():
                        target_character = CharacterService(target)
                        rs = target_character.impacted(action, calculated_impact, dice_result)
                        self.notifier.send_action_result(action, rs)
                        self.logger.debug(
                            f"Applied impact to target character {target.id} from action {action.id} in turn {self.turn.id}")
        self.turn.is_finished = True
        self.turn.save()
        self.logger.info(f"Turn {self.turn.id} is finished")

    def process(self):
        self.logger.info(f"Processing turn {self.turn.id}")
        self.check()
        self.prepare()
        self.play()
