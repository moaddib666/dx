import functools
import logging
import uuid
from functools import partial

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from apps.action.models import CharacterAction, DiceRollResult, ActionImpact
from apps.character.models import Character
from apps.core.bus.base import GameEvent
from apps.core.models import BriefCharacterInfo, AttributeType, AttributeHolder, CharacterStats, FullCharacterInfo, \
    FightSide, \
    ImpactType, ImpactViolationType, RollOutcome, Coordinate, EffectType, TheChosenPath, NormalizedCharacterPower, \
    SkillTypes, CharacterAbility
from apps.game.dto.impact import CalculatedImpact
from apps.game.exceptions import GameLogicException
from apps.game.services.character.character_abilities import can
from apps.game.services.character.character_normalizer import normalize_character_power
from apps.game.services.rand_dice import DiceService
from apps.school.models import Skill
from apps.shields.models import ActiveShield


class CharacterService:
    logger = logging.getLogger("game.services.character")

    def __init__(self, character: Character):
        self.character = character

    def get_dice_service(self) -> partial[DiceService]:
        return functools.partial(DiceService, self.character, self.get_stat(CharacterStats.LUCK))

    def roll_dice(self, sides: int) -> int:
        return self.get_dice_service()(sides=sides).roll()

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

    def increase_attribute(self, name: AttributeType | str, amount: int):
        if name == AttributeType.HEALTH:
            self.add_hp(amount)
        elif name == AttributeType.ENERGY:
            self.add_energy(amount)
        elif name == AttributeType.ACTION_POINTS:
            self.add_ap(amount)
        else:
            raise GameLogicException(f"Unknown attribute {name}")

    def spend_attribute(self, name: AttributeType | str, amount: int):
        if name == AttributeType.HEALTH:
            self.spend_hp(amount)
        elif name == AttributeType.ENERGY:
            self.spend_energy(amount)
        elif name == AttributeType.ACTION_POINTS:
            self.spend_ap(amount)
        else:
            raise GameLogicException(f"Unknown attribute {name}")

    def get_max_attribute(self, name: AttributeType | str) -> int:
        if name == AttributeType.HEALTH:
            return self.get_max_hp()
        elif name == AttributeType.ENERGY:
            return self.get_max_energy()
        elif name == AttributeType.ACTION_POINTS:
            return self.get_max_ap()
        else:
            raise GameLogicException(f"Unknown attribute {name}")

    def get_current_attribute(self, name: AttributeType | str) -> int:
        if name == AttributeType.HEALTH:
            return self.get_current_hp()
        elif name == AttributeType.ENERGY:
            return self.get_current_energy()
        elif name == AttributeType.ACTION_POINTS:
            return self.get_current_ap()
        else:
            raise GameLogicException(f"Unknown attribute {name}")

    def spend_all_ap(self):
        self.character.current_active_points = 0
        self.character.save(update_fields=['current_active_points'])

    def spend_ap(self, amount: int):
        self.character.current_active_points -= amount
        if self.character.current_active_points < 0:
            self.character.current_active_points = 0
        self.character.save(update_fields=['current_active_points'])

    def spend_energy(self, amount: int):
        self.character.current_energy_points -= amount
        if self.character.current_energy_points < 0:
            self.character.current_energy_points = 0
        self.character.save(update_fields=['current_energy_points'])

    def spend_hp(self, amount: int):
        self.character.current_health_points -= amount
        if self.character.current_health_points < 0:
            self.character.current_health_points = 0
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

    def get_character_info(self, refresh=True) -> FullCharacterInfo:
        if refresh:
            self.character.refresh_from_db()
        coordinates = Coordinate(
            x=0,
            y=0,
            z=0,
        )
        if self.character.position:
            coordinates = Coordinate(x=self.character.position.grid_x, y=self.character.position.grid_y,
                                     z=self.character.position.grid_z)
        return FullCharacterInfo(
            id=self.character.id,
            position=self.character.position_id,
            coordinates=coordinates,
            name=self.character.name,
            attributes=[
                self.get_attribute(attr_name) for attr_name in AttributeType
            ],
            dimension=self.character.dimension_id,
            rank_grade=self.character.rank.grade,
            # fight=None,
            # duel_invitations=self.character.duel_invitations_received.exclude(
            #     is_accepted=True, is_rejected=True, created_at__gte=timezone.now() - timedelta(minutes=5)
            # ).values_list('id', flat=True),

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
        modifier = self.character.stats_modifiers.filter(name=param).aggregate(models.Sum('value'))['value__sum'] or 0
        real_stat = self.get_real_stat(param)
        return real_stat + modifier

    def get_real_stat(self, param: CharacterStats) -> int:
        if param not in CharacterStats._value2member_map_:
            raise GameLogicException(f"Unknown stat {param}")
        # TODO: Calculate the impact if any
        try:
            return self.character.stats.get(name=param).value
        except ObjectDoesNotExist:
            return 0

    # TODO: refactor this
    def impacted(self, action: CharacterAction, calculated_impact: CalculatedImpact,
                 dice_roll_result: DiceRollResult):
        self.logger.debug(f"Character {self.character.id} impacted with {calculated_impact}")
        # FIXME: adjust to allow healing in knock out state
        if self.character.current_health_points <= 0 and calculated_impact['kind'] == ImpactType.DAMAGE:
            self.logger.debug(f"Character {self.character.id} is already dead")

        if calculated_impact['kind'] not in (ImpactType.DAMAGE, ImpactType.HEAL):
            raise GameLogicException(f"Unknown impact kind {calculated_impact['kind']}")

        self.character.current_health_points -= calculated_impact['value']
        if self.character.current_health_points < 0:
            self.character.current_health_points = 0
        if self.character.current_health_points > self.get_max_hp():
            self.character.current_health_points = self.get_max_hp()
        # safe roll
        if self.character.current_health_points <= 0:
            if dice_roll_result.outcome == RollOutcome.CRITICAL_FAIL:
                self.logger.info(f"Attacker {self.character.id} received critical fail and cant kill the target")
                self.character.current_health_points = 1
            # TODO: draw the dice d20 and if critical success heal it to 1hp
        self.character.save(update_fields=['current_health_points', 'updated_at'])
        self.logger.info(
            f"Character {self.character.id} received {calculated_impact['value']} of {calculated_impact['kind']} damage")

    def refill_all(self):
        self.refill_ap()
        self.refill_energy()
        self.refill_health()

    def refill_ap(self):
        self.character.current_active_points = self.get_max_ap()
        self.character.save(update_fields=['current_active_points', 'updated_at'])

    def refill_energy(self):
        self.character.current_energy_points = self.get_max_energy()
        self.character.save(update_fields=['current_energy_points', 'updated_at'])

    def refill_health(self):
        self.character.current_health_points = self.get_max_hp()
        self.character.save(update_fields=['current_health_points', 'updated_at'])

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

    def get_attribute_value(self, name: AttributeType | str) -> int:
        return self.get_attribute(name).current

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
        return False

    def get_fight_id(self):
        return self.character.fight_id

    def get_fight_team(self) -> FightSide:
        return self.character.fight.get_character_side(self.character)

    def has_effect(self, effect: EffectType) -> bool:
        return self.character.effects.filter(effect=effect, active=True).exists()

    def has_effects(self, effects: [EffectType]) -> bool:
        return self.character.effects.filter(effect__in=effects, active=True).exists()

    def get_shields(self) -> [ActiveShield]:
        return self.character.shields.all()

    def is_in_safe_place(self) -> bool:
        return self.character.position.is_safe

    def not_alone(self) -> bool:
        return Character.objects.filter(position=self.character.position, is_active=True).exclude(
            id=self.character.id).exists()

    @property
    def rank_grade(self) -> int:
        return self.character.rank.grade

    def __str__(self):
        return f"CharacterService({self.model})"

    def get_path(self) -> TheChosenPath:
        return self.character.path.name if self.character.path else TheChosenPath.NOT_CHOSEN

    @functools.lru_cache(1)
    def get_power_stats(self) -> NormalizedCharacterPower:
        """
        Cached method to get normalized character power.
        """
        return normalize_character_power(self)

    def can(self, skill_type: SkillTypes) -> CharacterAbility:
        return can(self, skill_type)
