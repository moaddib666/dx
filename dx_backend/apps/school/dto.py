import typing
import uuid
from typing import List, Optional

from typing_extensions import TypedDict

from apps.core.models import ImpactType, ImpactViolationType, AttributeType, CharacterStats, SkillTypes, EffectType


class StatRequirement(TypedDict):
    stat: CharacterStats
    value: int


class Scaling(TypedDict):
    stat: str
    value: float


class Formula(TypedDict):
    base: int
    requires: List[StatRequirement]
    scaling: List[Scaling]
    max_efficiency: Optional[float]
    min_efficiency: Optional[float]


class Impact(TypedDict):
    """
    [{"kind": "Damage", "type": "Heat", "formula": {"base": 15, "requires": [{"stat": "Flow Manipulation", "value": 5}], "scaling": [{"stat": "Flow Manipulation", "value": 0.2}]}}]
    """
    kind: ImpactType
    type: ImpactViolationType
    formula: Formula


class Cost(TypedDict):
    kind: AttributeType
    value: int


class Modifier(TypedDict):
    label: typing.AnyStr
    formula: Formula


class AssignableEffect(TypedDict):
    """
    {
        "name": "Burn",
        "base_chance": 0.1,
        "duration_modifier": {"value": 1, "formula": {"base": 1, "requires": [{"stat": "Flow Manipulation", "value": 5}], "scaling": [{"stat": "Flow Manipulation", "value": 0.2}]}},
        "stat_modifiers": [{"value": 5, "formula": {"base": 5, "requires": [{"stat": "Flow Manipulation", "value": 5}], "scaling": [{"stat": "Flow Manipulation", "value": 0.2}}}]
    }
    """
    name: EffectType
    impact: Optional[Impact]
    base_chance: float
    duration_modifier: Modifier
    stat_modifiers: List[Modifier]


class BaseSkill(TypedDict):
    name: str
    description: str
    school: uuid.UUID
    multi_target: bool
    type: SkillTypes
    grade: int
    cost: List[Cost]
    effect: List[AssignableEffect]
    impact: List[Impact]
