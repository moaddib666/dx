import datetime
import uuid
from enum import StrEnum
from typing import Optional, List

from polymorphic.models import PolymorphicModel
from pydantic import BaseModel


class DjangoChoicesMixin:
    @classmethod
    def choices(cls):
        return [(item.value, item.value) for item in cls]

    @classmethod
    @property
    def default(cls):
        return cls.choices()[0][0]


class GenderEnum(DjangoChoicesMixin, StrEnum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'


class CharacterActionType(DjangoChoicesMixin, StrEnum):
    USE_SKILL = "USE_SKILL"
    USE_ITEM = "USE_ITEM"
    DIMENSION_SHIFT = "DIMENSION_SHIFT"
    CHANGE_POSITION = "CHANGE_POSITION"
    START_DIALOGUE = "START_DIALOGUE"
    MAKE_DUEL_INVITATION = "MAKE_DUEL_INVITATION"
    ACCEPT_DUEL_INVITATION = "ACCEPT_DUEL_INVITATION"
    REJECT_DUEL_INVITATION = "REJECT_DUEL_INVITATION"
    START_FIGHT = "START_FIGHT"
    MOVE = "MOVE"
    DICE_ROLL = "DICE_ROLL"

    GIFT = "GIFT"
    ANOMALY = "ANOMALY"

    # GM ACTIONS
    GOD_INTERVENTION = "GOD_INTERVENTION"

    # SPECIAL ACTIONS
    LONG_REST = "LONG_REST"
    BACK_TO_SAFE_ZONE = "BACK_TO_SAFE_ZONE"
    INSPECT = "INSPECT"
    SNATCH = "SNATCH_ITEM"


class CharacterSpecialActionType(DjangoChoicesMixin, StrEnum):
    INSPECT = "INSPECT"
    SNATCH = "SNATCH_ITEM"
    BARGAIN = "BARGAIN"
    GIFT = "GIFT"
    # BUY_ITEM = "BUY_ITEM"
    LONG_REST = "LONG_REST"
    BACK_TO_SAFE_ZONE = "BACK_TO_SAFE_ZONE"


class SpecialSkillType(DjangoChoicesMixin, StrEnum):
    REGULAR_ACTION = "ACTION"
    TELEPORT = "TELEPORT"
    TELEPORT_TO_CHARACTER = "TELEPORT_TO_CHARACTER"
    TELEPORT_TO_SAFE_ZONE = "TELEPORT_TO_SAFE_ZONE"
    RESET_STATS = "RESET_STATS"
    FLOW_ACCUMULATION = "FLOW_ACCUMULATION"


class ItemType(DjangoChoicesMixin, StrEnum):
    WEAPON = 'weapon'
    ARMOR = 'armor'
    ARTIFACT = 'artifact'
    AMULET = 'amulet'
    MATERIAL = 'material'
    QUEST = 'quest'
    MISC = 'misc'
    FOOD = 'food'
    RUNE = 'rune'


class EffectType(DjangoChoicesMixin, StrEnum):
    KNOCKED_OUT = "Knocked out"  # Can be atacked in case damage is bigger that full health points character is in coma, can be healed by other players using healing spells or items
    COMA = "Coma"  # Can't be attacked or attack even healings are not working only time can heal or high level healers or resque packages
    NONE = "None"  # No effect
    BURNING = "Burning"  # Decrease health points every turn by fire damage
    POISONED = "Poisoned"  # Decrease health points every turn by poison damage
    SLEEPING = "Sleeping"  # Can't move or attack
    CONFUSED = "Confused"  # The character can't distinguish between friend and enemy targets allways random
    PARALYZED = "Paralyzed"  # Can't move or attack
    FEAR = "Fear"  # The concentration, mental strand is decreased
    SLOWNESS = "Slowness"  # Decrease speed
    COLD = "Cold"  # Decrease health points with ice damage every turn
    CURSED = "Cursed"  # Decrease luck points
    BLINDNESS = "Blindness"  # Decrease accuracy
    HASTE = "Haste"  # Increase speed
    REGENERATION = "Regeneration"  # Increase health points every turn
    BLESSED = "Blessed"  # Increase luck points
    ARCANE_SURGE = "Arcane Surge"  # Increase magic skills

    MARKED_FOR_DEATH = "Marked"  # The character is marked for being attacked by NPC


class EffectViolation(DjangoChoicesMixin, StrEnum):
    NONE = "None"
    Negative = "Negative"
    Positive = "Positive"
    Neutral = "Neutral"
    Special = "Special"


class SkillTypes(DjangoChoicesMixin, StrEnum):
    ATTACK = 'attack'
    DEFENSE = 'defense'
    HEAL = 'heal'
    BUFF = 'buff'
    DEBUFF = 'debuff'
    UTILITY = 'utility'
    SPECIAL = 'special'


class ImpactType(DjangoChoicesMixin, StrEnum):
    NONE = "None"
    KNOCK_OUT = "Knock out"

    DAMAGE = "Damage"
    HEAL = "Heal"
    SHIELD = "Shield"

    BUFF = "Buff"
    DEBUFF = "Debuff"

    STUN = "Stun"
    SLEEP = "Sleep"
    CONFUSION = "Confusion"
    PARALYSIS = "Paralysis"

    FEAR = "Fear"

    FREEZE = "Freeze"
    BURN = "Burn"
    POISON = "Poison"

    SLOW = "Slow"
    HASTE = "Haste"

    BLIND = "Blind"
    SILENCE = "Silence"
    BLEED = "Bleed"
    DISARM = "Disarm"
    ROOT = "Root"

    ENERGY_DECREASE = "Energy Decrease"

    REFLECT = "Reflect"
    ABSORB = "Absorb"
    DODGE = "Dodge"
    RESIST = "Resist"
    IMMUNITY = "Immunity"
    REGENERATION = "Regeneration"
    LIFESTEAL = "Lifesteal"


class ImpactViolationType(DjangoChoicesMixin, StrEnum):
    PHYSICAL = "Physical"  # Basic impact, e.g., hit in the face with a ball
    MENTAL = "Mental"  # Affects perception and interaction, e.g., induced fear
    ENERGY = "Energy"  # Flow-based impact, e.g., hit by an energy beam
    HEAT = "Heat"  # Exposure to high temperatures, e.g., sunburn
    COLD = "Cold"  # Exposure to low temperatures, e.g., frostbite
    LIGHT = "Light"  # Intense light exposure, affecting vision or causing burns
    DARKNESS = "Darkness"  # Prolonged darkness exposure, causing disorientation or fear
    NONE = "None"  # No violation, e.g., healing or buffing


class DirectionEnum(DjangoChoicesMixin, StrEnum):
    NORTHWEST = "North-West"
    NORTH = "North"
    NORTH_EAST = "North-East"

    EAST = "East"
    WEST = "West"

    SOUTH_WEST = "South-West"
    SOUTH = "South"
    SOUTH_EAST = "South-East"

    UP = "Up"
    DOWN = "Down"


class LifePath(DjangoChoicesMixin, StrEnum):
    PATH_OF_TECH = "Tech"
    PATH_OF_MAGIC = "Magic"


class CalculatedImpact(BaseModel):
    kind: ImpactViolationType
    value: int


class CharacterStats(DjangoChoicesMixin, StrEnum):
    PHYSICAL_STRENGTH = "Physical Strength"  # Influences health and physical damage
    MENTAL_STRENGTH = "Mental Strength"  # Influences energy and mental resilience
    FLOW_RESONANCE = "Flow Resonance"  # Ability to align with the Flow, enhancing spell potency

    CONCENTRATION = "Concentration"  # Ability to maintain spell casting under pressure
    FLOW_MANIPULATION = "Flow Manipulation"  # Skill in shaping and controlling Flow energy
    FLOW_CONNECTION = "Flow Connection"  # Depth of bond with the Flow, affecting spell efficiency

    KNOWLEDGE = "Knowledge"  # Understanding of magical theory and applications

    SPEED = "Speed"  # Influences action points and turn order
    LUCK = "Luck"  # Adds a modifier to various outcomes
    CHARISMA = "Charisma"  # Ability to influence others and maintain relationships


class RegisteredDiceRoll(BaseModel):
    dice_side: int
    outcome: str


class RegisteredImpact(BaseModel):
    """
     {
          "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "dice_roll_result": {
            "dice_side": 9223372036854776000,
            "outcome": "Critical Fail"
          },
          "type": "None",
          "violation": "Physical",
          "size": 9223372036854776000,
          "target": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }
    """
    id: uuid.UUID
    dice_roll_result: RegisteredDiceRoll
    type: ImpactType
    violation: ImpactViolationType
    size: int
    target: uuid.UUID


class CharacterStatHolder(BaseModel):
    name: CharacterStats
    value: int


class AttributeType(DjangoChoicesMixin, StrEnum):
    HEALTH = "Health"
    ENERGY = "Energy"
    ACTION_POINTS = "Action Points"


class AttributeHolder(BaseModel):
    name: AttributeType
    current: Optional[int]
    max: Optional[int]


class BriefCharacterInfo(BaseModel):
    id: uuid.UUID
    name: str
    attributes: list[AttributeHolder]
    dimension: int
    rank_grade: int


class CharacterInspectInfo(BaseModel):
    id: uuid.UUID
    name: str
    attributes: list[AttributeHolder]
    dimension: int
    rank_grade: Optional[int]
    path: Optional[uuid.UUID]

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data["id"] = str(data["id"])
        data["path"] = str(data["path"])
        return data


class SnatchResult(BaseModel):
    target: uuid.UUID
    success: bool
    discovered: List[uuid.UUID]
    snatched: List[uuid.UUID]


class MultipleSnatchResult(BaseModel):
    targets: List[SnatchResult]


class MultipleCharacterInspectInfo(BaseModel):
    characters: list[CharacterInspectInfo]


class DimensionInfo(BaseModel):
    id: str
    name: str
    speed: float


class RankInfo(BaseModel):
    name: str
    grade: int
    current_experience: int
    next_rank_experience: int


class CharacterBio(BaseModel):
    age: int
    gender: GenderEnum
    appearance: str
    background: str


class CharacterTemplateValidator(BaseModel):
    max_stats_points_count: int
    max_modificators_count: int
    max_items_count: int
    max_spells_count: int
    max_rank_grade: int
    max_schools_count: int


class CharacterGenericData(BaseModel):
    """
    {
      "name": "Zena",
      "tags": ["clever", "intelligent"],
      "bio": {
        "age": 25,
        "gender": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
        "appearance": "Tall, dark hair, green eyes",
        "background": "Zena is a young magician who has been studying the flow for the past 5 years. She is a quick learner and has a natural talent for manipulating the flow. She is currently on a quest to find the lost artifacts of the ancient flow masters."
      },
      "rank": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
      "path": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
      "stats": [
        {
          //      "PHYSICAL_STRENGTH": 10,
          //      "MENTAL_STRENGTH": 10,
          //      "LUCK": 12,
          //      "SPEED": 15,
          //      "CONCENTRATION": 10,
          //      "FLOW_MANIPULATION": 8,
          //      "FLOW_CONNECTION": 7,
          //      "KNOWLEDGE": 10,
          //      "FLOW_RESONANCE": 6,
          //      "CHARISMA": 7
          "id": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "name": "PHYSICAL_STRENGTH",
          "value": 10
        }
      ],
      "modificators": [
        {
          "id": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "name": "Moralist"
        }
      ],
      "currencyTokens": [
        {
          "id": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "name": "Generic Token",
          "value": 10
        },
        {
          "id": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "name": "Dark Token",
          "value": 1
        }
      ],
      "items": [
        {
          "id": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "name": "Touched with the fow dagger",
          "type": "weapon"
        },
        {
          "id": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "name": "Magnetic Shield",
          "type": "armor"
        },
        {
          "id": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "name": "Small Flow Artifact",
          "type": "artifact"
        },
        {
          "id": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "name": "Small Flow Artifact",
          "type": "artifact"
        }
      ],
      "shools": [
        {
          "id": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "name": "Magician Basics",
          "level": 1
        },
        {
          "id": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "name": "Flow Manipulation",
          "level": 1
        },
        {
          "id": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "name": "Flow Connection",
          "level": 1
        }
      ],
      "spells": [
        {
          "id": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "name": "Flow Shield",
          "school": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "level": 1
        },
        {
          "id": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "name": "Flow Accumulation",
          "school": "b1b1b1b1-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
          "level": 1
        }
      ]
    }

    """
    name: str
    tags: list[str]
    bio: CharacterBio
    rank: int
    path: Optional[uuid.UUID]
    stats: list[CharacterStatHolder]
    modificators: list[uuid.UUID]
    items: list[uuid.UUID]
    schools: list[uuid.UUID]
    spells: list[int]


class CharacterTemplate(BaseModel):
    data: CharacterGenericData
    validation: CharacterTemplateValidator


class Coordinate(BaseModel):
    x: int
    y: int
    z: int


class FullCharacterInfo(BaseModel):
    id: uuid.UUID
    name: str
    rank_grade: int

    attributes: list[AttributeHolder]
    # path: LifePath

    dimension: int
    # location: uuid.UUID
    position: uuid.UUID
    coordinates: Optional[Coordinate]
    # fight: Optional[uuid.UUID]
    # duel_invitations: list[uuid.UUID]


class RollOutcome(DjangoChoicesMixin, StrEnum):
    CRITICAL_FAIL = "Critical Fail"
    CRITICAL_SUCCESS = "Critical Success"
    BAD_LUCK = "Bad Luck"
    BASE_VALUE = "Base Value"
    GOOD_LUCK = "Good Luck"


class DiceRollResult(BaseModel):
    dice_side: int
    multiplier: Optional[float]
    outcome: RollOutcome

    class Config:
        from_attributes = True


class CurrentTurn(BaseModel):
    id: uuid.UUID
    started_at: datetime.datetime
    duration: int


class TurnFinished(BaseModel):
    id: uuid.UUID
    ended_at: datetime.datetime
    next_turn_id: uuid.UUID
    turn_duration: int


class ActionModel(BaseModel):
    action_type: CharacterActionType
    initiator_id: uuid.UUID

    skill_id: Optional[int]
    target_dimension_id: Optional[uuid.UUID]
    target_location_id: Optional[uuid.UUID]

    class Config:
        from_attributes = True


class ActionImpactModel(BaseModel):
    type: ImpactType
    violation: ImpactViolationType
    size: int
    dice_roll_result: DiceRollResult

    class Config:
        from_attributes = True


FIGHT_TURN_DURATION_SECONDS = 30


class FightSide(DjangoChoicesMixin, StrEnum):
    ATTACKER = "Attacker"
    DEFENDER = "Defender"


class GameMasterImpactAction(BaseModel):
    initiator: uuid.UUID
    target: uuid.UUID
    impact_type: ImpactType
    impact_violation: ImpactViolationType


from apps.core.utils.models import BaseModel as DjangoBaseModel, TagsDescriptor
from django.db import models as django_models


class GameObject(DjangoBaseModel, PolymorphicModel):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
    position = django_models.ForeignKey("world.Position", null=True, on_delete=django_models.SET_NULL, blank=True,
                                        default=None)
    dimension = django_models.ForeignKey("world.Dimension", on_delete=django_models.SET_NULL, null=True, blank=True,
                                         default=1)
    is_active = django_models.BooleanField(default=True)
    campaign = django_models.ForeignKey('game.Campaign', on_delete=django_models.SET_NULL, null=True, blank=True,
                                        default=None)


class StatObject(DjangoBaseModel, PolymorphicModel):
    id = django_models.CharField(choices=CharacterStats.choices(), max_length=100, primary_key=True)
    icon = django_models.ImageField(upload_to='icons/stats/', null=True, blank=True)
    description = django_models.TextField(null=True, blank=True)


class ViolationObject(DjangoBaseModel, PolymorphicModel):
    id = django_models.CharField(choices=ImpactViolationType.choices(), max_length=100, primary_key=True)
    icon = django_models.ImageField(upload_to='icons/violation/', null=True, blank=True)
    description = django_models.TextField(null=True, blank=True)


class BehaviorModel(DjangoChoicesMixin, StrEnum):
    PASSIVE = "Passive"  # Disabled NPC Interaction
    AGGRESSIVE = "Aggressive"  # Attack when in range
    FRIENDLY = "Friendly"  # Help when in range


class DimensionAnomalyInteractionResult(BaseModel):
    gained_items: List[uuid.UUID]  # Items obtained from the anomaly
    gained_impacts: List[ActionImpactModel]  # Impacts applied to characters or objects
    dice_roll_result: Optional[DiceRollResult]  # Result of the dice roll during interaction


class DimensionAnomalyEffect(DjangoChoicesMixin, StrEnum):
    Positive = "Positive"  # Enhances characters and objects within its range
    Negative = "Negative"  # Harms characters and objects within its range
    Neutral = "Neutral"  # Does not affect characters and objects within its range


class DimensionAnomaly(GameObject):
    """
    Represents a dimension anomaly that can affect characters and objects within its range.
    """
    known = django_models.BooleanField(default=False)  # Indicates if the anomaly is known to the players and could be
    # deleted afer all actions of cuurent turn done
    level = django_models.PositiveIntegerField(default=1)
    effect = django_models.CharField(choices=DimensionAnomalyEffect.choices(), max_length=50,
                                     default=DimensionAnomalyEffect.Positive)


class GodInterventionSize(DjangoChoicesMixin, StrEnum):
    """
    Size indicates the magnitude of the god_intervention_service's impact on characters.
    Example sizes:
    - SMALL: Minor god_intervention_service 10-20% boost to attributes
    - MEDIUM: Moderate god_intervention_service 20-50% boost to attributes
    - LARGE: Major god_intervention_service 50-100% boost to attributes
    - GOD: Divine god_intervention_service 100%+ boost to attributes, potentially game-changing
    """
    SMALL = "Small"  # Minor god_intervention_service, small impact
    MEDIUM = "Medium"  # Moderate god_intervention_service, noticeable impact
    LARGE = "Large"  # Major god_intervention_service, significant impact
    GOD = "God"  # Divine god_intervention_service, maximum impact

    @classmethod
    def to_float(cls, size: 'GodInterventionSize') -> float:
        """
        Convert the GodInterventionSize to a float percentage.

        Args:
            size (GodInterventionSize): The size of the god_intervention_service.

        Returns:
            float: The percentage impact of the god_intervention_service.
        """
        if size == cls.SMALL:
            return 0.1
        elif size == cls.MEDIUM:
            return 0.25
        elif size == cls.LARGE:
            return 0.5
        elif size == cls.GOD:
            return 1.0
        else:
            raise ValueError(f"Unknown GodInterventionSize: {size}")

    def float_value(self) -> float:
        """
        Get the float value of the GodInterventionSize instance.

        Returns:
            float: The percentage impact of the god_intervention_service.
        """
        return self.to_float(self)


class GodInterventionType(DjangoChoicesMixin, StrEnum):
    """
    Type of god_intervention_service that can be applied to characters.
    Example types:
    - BLESSING: Positive god_intervention_service that boosts attributes
    - CURSE: Negative god_intervention_service that hinders attributes
    """
    BLESSING = "Blessing"  # Positive god_intervention_service, boosts attributes
    CURSE = "Curse"  # Negative god_intervention_service, hinders attributes

    def is_curse(self) -> bool:
        """
        Check if the god_intervention_service is a curse.

        Returns:
            bool: True if the god_intervention_service is a curse, False otherwise.
        """
        return self == GodInterventionType.CURSE

    def is_blessing(self) -> bool:
        """
        Check if the god_intervention_service is a blessing.

        Returns:
            bool: True if the god_intervention_service is a blessing, False otherwise.
        """
        return self == GodInterventionType.BLESSING


class GodIntervention(BaseModel):
    """
    Represents a god_intervention_service that can be applied to characters and boost their attributes.
    """
    type: GodInterventionType  # Type of the god_intervention_service (BLESSING or CURSE)
    size: GodInterventionSize
    attributes: List[AttributeType]


class MoveTypes(DjangoChoicesMixin, StrEnum):
    """
    Move types for NPC and character movement.
    Example move types:
    Teleport: Instantly moves to the target character's location
    Walk: Follows the target character by walking to their location
    """
    TELEPORT = "Teleport"
    WALK = "Walk"


class NormalizedCharacterPower(BaseModel):
    """
    Normalized character information for internal calculations and processing.

    - Max Power is a float value of computed character power based on the char attributes, stats, skills and items.
    - Current Power is a float value of computed character power computed based on current stats, skills and items.
    """
    id: uuid.UUID
    max_power: float
    current_power: float


class TheChosenPath(DjangoChoicesMixin, StrEnum):
    TECH_JOHN = "Path of John"
    MAGIC_JSON = "Path of JSon"
    NOT_CHOSEN = "Not Chosen"


class CharacterAbility(BaseModel):
    type: SkillTypes
    skills: List[int]  # List of learned skill IDs that the character can use
    items: List[uuid.UUID]  # List of item IDs that the character possesses

    def has_ability(self) -> bool:
        """
        Check if the character has any skills or items for this ability type.

        Returns:
            bool: True if the character has skills or items for this ability type, False otherwise.
        """
        return bool(self.skills or self.items)
