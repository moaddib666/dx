import typing as t
import uuid

from pydantic import BaseModel, Field

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

    # Use default_factory to avoid shared mutable defaults
    modifiers: t.List["ChallengeModifier"] = Field(default_factory=list)

    class Config:
        from_attributes = True


class ChallengeModifier(BaseModel):
    id: uuid.UUID
    name: str
    icon: t.Optional[str] = None
    value: int

    class Config:
        from_attributes = True


class ChallengeCreationRequest(BaseModel):
    """DTO for creating challenges."""
    target_character_id: uuid.UUID
    difficulty: int = 12
    dice_sides: int = 20
    stat: CharacterStats = CharacterStats.LUCK
    advantage: bool = False
    disadvantage: bool = False
    description: t.Optional[str] = None
    modifiers: t.List[uuid.UUID] = Field(default_factory=list)
