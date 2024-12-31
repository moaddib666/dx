from typing import TypedDict

from apps.core.models import ImpactType, ImpactViolationType


class CalculatedImpact(TypedDict):
    kind: ImpactType
    violation: ImpactViolationType
    value: int
