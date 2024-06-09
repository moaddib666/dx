from typing import List

from typing_extensions import TypedDict


class StatRequirement(TypedDict):
    stat: str
    value: float


class Scaling(TypedDict):
    stat: str
    value: float


class Formula(TypedDict):
    base: int
    requires: List[StatRequirement]
    scaling: List[Scaling]


class Impact(TypedDict):
    kind: str
    type: str
    formula: Formula


class Cost(TypedDict):
    kind: str
    value: int


class Effect(TypedDict):
    name: str
    chance: float
    durationSeconds: int
    description: str
