import logging
import random
import uuid
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from apps.action.models import CharacterAction, DiceRollResult, ActionImpact
from apps.character.models import Character
from apps.core.bus.base import GameEvent
from apps.core.models import BriefCharacterInfo, AttributeType, AttributeHolder, CharacterStats, FullCharacterInfo, \
    FightSide, \
    ImpactType, ImpactViolationType, RollOutcome, Coordinate, EffectType
from apps.game.dto.impact import CalculatedImpact
from apps.game.exceptions import GameLogicException
from apps.school.models import Skill


class CharacterService:
    logger = logging.getLogger("game.services.character")

    def __init__(self, character: Character):
        self.character = character

    @property
    def model(self):
        return self.character

    def knock_out(self):
        self.character.current_health_points = 0
        self.character.current_active_points = 0
        self.character.current_energy_points = 0
        self.character.save(
            update_fields=['current_health_points', 'current_active_points', 'current_energy_points', 'updated_at']
        )

    def spend_all_ap(self):
        self.character.current_active_points = 0
        self.character.save(update_fields=['current_active_points'])

    def spend_ap(self, amount: int):
        self.character.current_active_points -= amount
        self.character.save(update_fields=['current_active_points'])

    def spend_energy(self, amount: int):
        self.character.current_energy_points -= amount
        self.character.save(update_fields=['current_energy_points'])

    def spend_hp(self, amount: int):
        self.character.current_health_points -= amount
        self.character.save(update_fields=['current_health_points'])

    def add_hp(self, amount: int):
        current_hp = self.character.current_health_points
        max_hp = self.get_max_hp()
        if current_hp + amount > max_hp:
            self.character.current_health_points = max_hp
        else:
            self.character.current_health_points += amount
        self.character.save(update_fields=['current_health_points', 'updated_at'])

    def add_ap(self, amount: int):
        current_ap = self.character.current_active_points
        max_ap = self.get_max_ap()
        if current_ap + amount > max_ap:
            self.character.current_active_points = max_ap
        else:
            self.character.current_active_points += amount
        self.character.save(update_fields=['current_active_points', 'updated_at'])

    def add_energy(self, amount: int):
        current_energy = self.character.current_energy_points
        max_energy = self.get_max_energy()
        if current_energy + amount > max_energy:
            self.character.current_energy_points = max_energy
        else:
            self.character.current_energy_points += amount
        self.character.save(update_fields=['current_energy_points', 'updated_at'])

    def get_max_ap(self):
        return int(round(self.get_stat(CharacterStats.SPEED) * 0.5 * self.character.dimension.speed))

    def get_max_hp(self):
        strength = self.get_stat(CharacterStats.PHYSICAL_STRENGTH)
        # TODO: think about better formula for calculating max hp
        calculated_hp = round(strength * 7.5)
        return calculated_hp

    def get_max_energy(self):
        mental_strength = self.get_stat(CharacterStats.MENTAL_STRENGTH)
        # TODO: think about better formula for calculating max energy
        calculated_energy = 100 + round(mental_strength * 5.5)
        return calculated_energy

    def get_current_ap(self) -> int:
        return self.character.current_active_points

    def get_current_hp(self) -> int:
        return self.character.current_health_points

    def get_current_energy(self) -> int:
        return self.character.current_energy_points

    def get_character_info(self) -> FullCharacterInfo:
        self.character.refresh_from_db()
        return FullCharacterInfo(
            id=self.character.id,
            position=self.character.position_id,
            coordinates=Coordinate(x=self.character.position.grid_x, y=self.character.position.grid_y,
                                   z=self.character.position.grid_z),
            name=self.character.name,
            attributes=[
                self.get_attribute(attr_name) for attr_name in AttributeType
            ],
            dimension=self.character.dimension_id,
            rank_grade=self.character.rank.grade,
            fight=self.character.fight_id,
            duel_invitations=self.character.duel_invitations_received.exclude(
                is_accepted=True, is_rejected=True, created_at__gte=timezone.now() - timedelta(minutes=5)
            ).values_list('id', flat=True),

        )

    def notify(self, message: GameEvent):
        self.logger.info(f"Sending notification to {self.character.name}: {message}")

    def chose_path(self, path):
        if self.character.path:
            raise GameLogicException("Character already chose a path")
        if self.character.rank.grade == 0:
            raise GameLogicException("Character must reach rank 1 to choose a path")
        self.character.path = path
        self.character.save()

    def has_skill(self, skill_id: uuid.UUID):
        try:
            self.character.learned_skills.get(skill_id=skill_id)
        except Skill.DoesNotExist:
            raise GameLogicException("Character does not have skill")

    def get_current_speed(self) -> float:
        return self.get_stat(CharacterStats.SPEED) * self.character.dimension.speed

    def get_stat(self, param: CharacterStats) -> int:
        if param not in CharacterStats._value2member_map_:
            raise GameLogicException(f"Unknown stat {param}")
        # TODO: Calculate the impact if any
        try:
            return self.character.stats.get(name=param).value
        except ObjectDoesNotExist:
            return 0

    # TODO: refactor this
    def impacted(self, action: CharacterAction, calculated_impact: CalculatedImpact,
                 dice_roll_result: DiceRollResult) -> \
            list[ActionImpact]:
        results = []
        self.logger.debug(f"Character {self.character.id} impacted with {calculated_impact}")
        # FIXME: adjust to allow healing in knock out state
        if self.character.current_health_points <= 0 and calculated_impact['kind'] == ImpactType.DAMAGE:
            self.logger.debug(f"Character {self.character.id} is already dead")
            return results
        if action.skill.type == Skill.Types.SPECIAL:
            self.logger.debug(f"Special skill impact")
            # FIXME: dirty hack
            if action.skill.id == 167:
                self.logger.debug(f"Special skill impact accumulate energy")
                self.add_energy(int(self.get_max_energy() * (random.randint(1, 10) / 10)))
            return results

        # FIXME: add processing for other impact types
        if calculated_impact['kind'] not in (ImpactType.DAMAGE, ImpactType.HEAL):
            raise GameLogicException(f"Unknown impact kind {calculated_impact['kind']}")

        self.character.current_health_points -= calculated_impact['value']
        if self.character.current_health_points < 0:
            self.character.current_health_points = 0
        if self.character.current_health_points > self.get_max_hp():
            self.character.current_health_points = self.get_max_hp()
        self.character.save()
        r = action.impacts.create(
            target=self.character,
            type=calculated_impact["kind"],
            violation=ImpactViolationType.PHYSICAL,  # FIXME
            size=calculated_impact['value'],
            dice_roll_result=dice_roll_result
        )
        results.append(r)
        if self.character.current_health_points <= 0:
            if dice_roll_result.outcome == RollOutcome.CRITICAL_FAIL:
                self.character.current_health_points = 1
                self.character.save()
            # TODO: draw the dice d20 and if critical success heal it to 1hp
            else:
                r = action.impacts.create(
                    target=self.character,
                    type=ImpactType.KNOCK_OUT,
                    violation=ImpactViolationType.PHYSICAL,  # FIXME
                    size=0,
                    dice_roll_result=dice_roll_result
                )
                results.append(r)
        self.logger.info(
            f"Character {self.character.id} received {calculated_impact['value']} of {calculated_impact['kind']} damage")
        return results

    def refill_all(self):
        self.refill_ap()
        self.refill_energy()
        self.refill_health()

    def refill_ap(self):
        self.character.current_active_points = self.get_max_ap()
        self.character.save()

    def refill_energy(self):
        self.character.current_energy_points = self.get_max_energy()
        self.character.save()

    def refill_health(self):
        self.character.current_health_points = self.get_max_hp()
        self.character.save()

    # TODO: move this to the dimension service
    def dimension_shift(self, action: CharacterAction) -> ActionImpact:
        self.character.dimension = action.target_dimension
        self.character.save()
        cost = 0

        if self.character.dimension.id > action.target_dimension.id:
            cost = action.target_dimension.shift_cost

        result = action.impacts.create(
            target=self.character,
            type=ImpactType.ENERGY_DECREASE,
            value=action.target_dimension.id,
            violation=ImpactViolationType.NONE,
        )
        self.character.current_energy_points -= cost
        self.character.save()
        return result

    def get_attribute(self, name: AttributeType | str) -> AttributeHolder:
        if name == AttributeType.HEALTH:
            return AttributeHolder(name=name, current=self.character.current_health_points, max=self.get_max_hp())
        if name == AttributeType.ENERGY:
            return AttributeHolder(name=name, current=self.character.current_energy_points, max=self.get_max_energy())
        if name == AttributeType.ACTION_POINTS:
            return AttributeHolder(name=name, current=self.character.current_active_points, max=self.get_max_ap())
        raise GameLogicException(f"Unknown attribute {name}")

    def get_brief_info(self) -> BriefCharacterInfo:
        return BriefCharacterInfo(
            id=self.character.id,
            name=self.character.name,
            attributes=[
                self.get_attribute(attr_name) for attr_name in AttributeType
            ],
            dimension=self.character.dimension.id,
            rank_grade=self.character.rank.grade,
        )

    def is_knocked_out(self) -> bool:
        return self.character.current_health_points <= 0

    def get_id(self) -> str:
        return str(self.character.id)

    def in_fight(self) -> bool:
        return self.character.fight_id is not None

    def get_fight_id(self):
        return self.character.fight_id

    def get_fight_team(self) -> FightSide:
        return self.character.fight.get_character_side(self.character)

    def has_effect(self, effect: EffectType) -> bool:
        return self.character.effects.filter(effect=effect, active=True).exists()

    def has_effects(self, effects: [EffectType]) -> bool:
        return self.character.effects.filter(effect__in=effects, active=True).exists()
