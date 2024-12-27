from typing import List

from typing_extensions import TypedDict

from apps.core.models import ImpactType, ImpactViolationType, AttributeType, CharacterStats


class StatRequirement(TypedDict):
    stat: CharacterStats
    value: float


class Scaling(TypedDict):
    stat: str
    value: float


class Formula(TypedDict):
    base: int
    requires: List[StatRequirement]
    scaling: List[Scaling]


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


class Effect(TypedDict):
    name: str
    chance: float
    durationSeconds: int
    description: str
