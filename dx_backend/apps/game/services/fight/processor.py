import logging
from django.db import transaction
from apps.fight.models import Fight, FightTurn, FightTurnAction
from apps.game.exceptions import GameLogicException
from apps.game.services.player.core import PlayerService
from apps.game.services.rand_dice import DiceService
from apps.game.services.skills.cost_validator import SkillCostService
from apps.game.services.skills.impact_calculator import SkillImpactService


class FightPlayerService:
    logger = logging.getLogger("game.services.fight")

    def __init__(self, fight: Fight):
        self.fight = fight

    def process_current_turn(self):
        self.logger.info(f"Processing current turn for fight {self.fight.id}")
        TurnProcessorService(self.fight.current_turn).process()

    def fill_up_players_ap(self):
        self.logger.info(f"Filling up players AP for fight {self.fight.id}")
        for participant in (
                self.fight.side_b_participants.all()
                | self.fight.side_a_participants.all()
                        .filter(current_health_points__gt=0)
        ):
            player = PlayerService(participant)
            player.refill_ap()
            self.logger.debug(f"Refilled AP for player {participant.id}")

    def spawn_turn(self):
        self.logger.info(f"Spawning new turn for fight {self.fight.id}")
        previous_turn = self.fight.current_turn
        previous_turn.refresh_from_db()
        if previous_turn and not previous_turn.is_finished:
            self.logger.error(f"Previous turn {previous_turn.id} is not finished")
            raise GameLogicException("Previous turn is not finished")
        turn = FightTurn.objects.create(fight=self.fight)
        self.fight.current_turn = turn
        self.fight.save()
        self.logger.info(f"Spawned new turn {turn.id} for fight {self.fight.id}")
        self.fill_up_players_ap()

    @transaction.atomic
    def process(self):
        self.logger.info(f"Processing fight {self.fight.id}")
        if self.fight.current_turn:
            self.process_current_turn()
        self.spawn_turn()


class TurnProcessorService:
    logger = logging.getLogger("game.services.turn_processor")

    def __init__(self, turn: FightTurn):
        self.turn = turn

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
        player: PlayerService | None = None
        for action in skills:
            skill = action.skill
            skill_require_ap = SkillCostService(skill).get_ap_cost()
            if not player or player.player.pk != action.initiator_id:
                player = PlayerService(action.initiator)
                time_taken = 0
            time_taken += skill_require_ap * 100 / player.get_current_speed()
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
            initiator = PlayerService(action.initiator)
            if action.action_type == FightTurnAction.ActionType.dimension_shift:
                initiator.dimension_shift(action.target_dimension)
                self.logger.debug(f"Processed dimension shift action {action.id} for turn {self.turn.id}")
                continue
            if action.action_type == FightTurnAction.ActionType.use_skill:
                calculated_impacts = SkillImpactService(action.skill, initiator).calculate_impact()
                multiplier = DiceService(initiator.player, initiator.get_stat("luck")).calculate_multiplier()
                for calculated_impact in calculated_impacts:
                    calculated_impact['value'] = int(calculated_impact['value'] * multiplier[1])
                    self.logger.debug(
                        f"Calculated impact damage {calculated_impact['value']} for action {action.id} in turn {self.turn.id}")
                    for target in action.targets.all():
                        target_player = PlayerService(target)
                        target_player.impacted(calculated_impact)
                        self.logger.debug(
                            f"Applied impact to target player {target.id} from action {action.id} in turn {self.turn.id}")
        self.turn.is_finished = True
        self.turn.save()
        self.logger.info(f"Turn {self.turn.id} is finished")

    def process(self):
        self.logger.info(f"Processing turn {self.turn.id}")
        self.check()
        self.prepare()
        self.play()
