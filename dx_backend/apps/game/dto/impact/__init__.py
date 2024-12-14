from typing import TypedDict

from apps.core.models import ImpactType


class CalculatedImpact(TypedDict):
    kind: ImpactType
    value: int
