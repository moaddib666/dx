import typing as t
import uuid

from pydantic import BaseModel

from apps.core.models import CharacterStats
from apps.core.models import DiceRollResult


class Challenge(BaseModel):
    id: uuid.UUID
    target_id: uuid.UUID
    difficulty: int = 12
    description: t.Optional[str] = None
    dice_sides: int = 20
    outcome: t.Optional["DiceRollResult"] = None
    stat: CharacterStats = CharacterStats.LUCK
    advantage: bool = False
    disadvantage: bool = False

    modifiers: t.List["ChallengeModifier"] = []


class ChallengeModifier(BaseModel):
    name: str
    icon: t.Optional[str] = None
    value: int
