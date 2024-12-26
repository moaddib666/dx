import datetime
import uuid
from enum import StrEnum
from typing import Optional

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
    BACK_TO_SAFE_ZONE = "BACK_TO_SAFE_ZONE"
    DICE_ROLL = "DICE_ROLL"


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
    LUCK = "Luck"  # Adds a modifier to various outcomes
    SPEED = "Speed"  # Influences action points and turn order
    CONCENTRATION = "Concentration"  # Ability to maintain spell casting under pressure
    FLOW_MANIPULATION = "Flow Manipulation"  # Skill in shaping and controlling Flow energy
    FLOW_CONNECTION = "Flow Connection"  # Depth of bond with the Flow, affecting spell efficiency
    KNOWLEDGE = "Knowledge"  # Understanding of magical theory and applications
    FLOW_RESONANCE = "Flow Resonance"  # Ability to align with the Flow, enhancing spell potency
    CHARISMA = "Charisma"  # Ability to influence others and maintain relationships


class CharacterStatHolder(BaseModel):
    name: CharacterStats
    value: int


class AttributeType(DjangoChoicesMixin, StrEnum):
    HEALTH = "Health"
    ENERGY = "Energy"
    ACTION_POINTS = "Action Points"


class AttributeHolder(BaseModel):
    name: AttributeType
    current: int
    max: int


class BriefCharacterInfo(BaseModel):
    id: uuid.UUID
    name: str
    attributes: list[AttributeHolder]
    dimension: int
    rank_grade: int


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


class FullCharacterInfo(BaseModel):
    id: uuid.UUID
    name: str
    rank_grade: int

    attributes: list[AttributeHolder]
    # path: LifePath

    dimension: int
    # location: uuid.UUID
    position: uuid.UUID
    fight: Optional[uuid.UUID]
    duel_invitations: list[uuid.UUID]


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
