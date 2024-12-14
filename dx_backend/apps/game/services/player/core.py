import logging
import uuid
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from apps.action.models import PlayerAction, DiceRollResult, ActionImpact
from apps.core.bus.base import GameEvent
from apps.core.models import BriefPlayerInfo, AttributeType, AttributeHolder, PlayerStat, FullPlayerInfo, FightSide, \
    ImpactType, ImpactViolationType, RollOutcome
from apps.game.dto.impact import CalculatedImpact
from apps.game.exceptions import GameLogicException
from apps.player.models import Player
from apps.school.models import Skill


class PlayerService:
    logger = logging.getLogger("game.services.player")

    def __init__(self, player: Player):
        self.player = player

    def get_max_ap(self):
        return int(round(self.get_stat(PlayerStat.SPEED) * 0.5 * self.player.dimension.speed))

    def get_max_hp(self):
        strength = self.get_stat(PlayerStat.PHYSICAL_STRENGTH)
        # TODO: think about better formula for calculating max hp
        calculated_hp = round(strength * 7.5)
        return calculated_hp

    def get_max_energy(self):
        mental_strength = self.get_stat(PlayerStat.MENTAL_STRENGTH)
        # TODO: think about better formula for calculating max energy
        calculated_energy = 100 + round(mental_strength * 5.5)
        return calculated_energy

    def get_player_info(self) -> FullPlayerInfo:
        self.player.refresh_from_db()
        return FullPlayerInfo(
            id=self.player.id,
            location=self.player.current_location_id,
            name=self.player.name,
            attributes=[
                self.get_attribute(attr_name) for attr_name in AttributeType
            ],
            dimension=self.player.dimension_id,
            rank_grade=self.player.rank.grade,
            fight=self.player.fight_id,
            duel_invitations=self.player.duel_invitations_received.exclude(
                is_accepted=True, is_rejected=True, created_at__gte=timezone.now() - timedelta(minutes=5)
            ).values_list('id', flat=True),
        )

    def notify(self, message: GameEvent):
        self.logger.info(f"Sending notification to {self.player.name}: {message}")

    def chose_path(self, path):
        if self.player.path:
            raise GameLogicException("Player already chose a path")
        if self.player.rank.grade == 0:
            raise GameLogicException("Player must reach rank 1 to choose a path")
        self.player.path = path
        self.player.save()

    def has_skill(self, skill_id: uuid.UUID):
        try:
            self.player.learned_skills.get(skill_id=skill_id)
        except Skill.DoesNotExist:
            raise GameLogicException("Player does not have skill")

    def get_current_speed(self) -> float:
        return self.get_stat(PlayerStat.SPEED) * self.player.dimension.speed

    def get_stat(self, param: PlayerStat) -> int:
        if param not in PlayerStat._value2member_map_:
            raise GameLogicException(f"Unknown stat {param}")
        # TODO: Calculate the impact if any
        try:
            return self.player.stats.get(name=param).value
        except ObjectDoesNotExist:
            return 0

    # TODO: refactor this
    def impacted(self, action: PlayerAction, calculated_impact: CalculatedImpact, dice_roll_result: DiceRollResult) -> \
            list[ActionImpact]:
        results = []
        self.logger.debug(f"Player {self.player.id} impacted with {calculated_impact}")
        if self.player.current_health_points <= 0:
            self.logger.debug(f"Player {self.player.id} is already dead")
            return results

        # FIXME: add processing for other impact types
        if calculated_impact['kind'] != ImpactType.DAMAGE:
            raise GameLogicException(f"Unknown impact kind {calculated_impact['kind'] }")

        self.player.current_health_points -= calculated_impact['value']
        self.player.save()
        r = action.impacts.create(
            target=self.player,
            type=calculated_impact["kind"],
            violation=ImpactViolationType.PHYSICAL,  # FIXME
            size=calculated_impact['value'],
            dice_roll_result=dice_roll_result
        )
        results.append(r)
        if self.player.current_health_points <= 0:
            if dice_roll_result.outcome == RollOutcome.CRITICAL_FAIL:
                self.player.current_health_points = 1
                self.player.save()
            # TODO: draw the dice d20 and if critical success heal it to 1hp
            else:
                r = action.impacts.create(
                    target=self.player,
                    type=ImpactType.KNOCK_OUT,
                    violation=ImpactViolationType.PHYSICAL,  # FIXME
                    size=0,
                    dice_roll_result=dice_roll_result
                )
                results.append(r)
        self.logger.info(
            f"Player {self.player.id} received {calculated_impact['value']} of {calculated_impact['kind']} damage")
        return results

    def refill_ap(self):
        self.player.current_active_points = self.get_max_ap()
        self.player.save()

    def refill_energy(self):
        self.player.current_energy_points = self.player.stats.energy_points
        self.player.save()

    def refill_health(self):
        self.player.current_health_points = self.player.stats.health_points
        self.player.save()

    # TODO: move this to the dimension service
    def dimension_shift(self, action: PlayerAction) -> ActionImpact:
        self.player.dimension = action.target_dimension
        self.player.save()
        cost = 0

        if self.player.dimension.id > action.target_dimension.id:
            cost = action.target_dimension.shift_cost

        result = action.impacts.create(
            target=self.player,
            type=ImpactType.ENERGY_DECREASE,
            value=action.target_dimension.id,
            violation=ImpactViolationType.NONE,
        )
        self.player.current_energy_points -= cost
        self.player.save()
        return result

    def get_attribute(self, name: AttributeType | str) -> AttributeHolder:
        if name == AttributeType.HEALTH:
            return AttributeHolder(name=name, current=self.player.current_health_points, max=self.get_max_hp())
        if name == AttributeType.ENERGY:
            return AttributeHolder(name=name, current=self.player.current_energy_points, max=self.get_max_energy())
        if name == AttributeType.ACTION_POINTS:
            return AttributeHolder(name=name, current=self.player.current_active_points, max=self.get_max_ap())
        raise GameLogicException(f"Unknown attribute {name}")

    def get_brief_info(self) -> BriefPlayerInfo:
        return BriefPlayerInfo(
            id=self.player.id,
            name=self.player.name,
            attributes=[
                self.get_attribute(attr_name) for attr_name in AttributeType
            ],
            dimension=self.player.dimension.id,
            rank_grade=self.player.rank.grade,
        )

    def is_knocked_out(self) -> bool:
        return self.player.current_health_points <= 0

    def get_id(self) -> str:
        return str(self.player.id)

    def in_fight(self) -> bool:
        return self.player.fight_id is not None

    def get_fight_id(self):
        return self.player.fight_id

    def get_fight_team(self) -> FightSide:
        return self.player.fight.get_player_side(self.player)
