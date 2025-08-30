import uuid
from typing import Optional, Union
from datetime import datetime

from apps.core.bus.base import GameEventData
from apps.core.models import CharacterActionType


class NewCycleData(GameEventData):
    id: int
    number: int
    campaign: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_current: bool


class ActionAcceptedData(GameEventData):
    id: uuid.UUID
    action_type: CharacterActionType

    cycle: dict
    order: float

    initiator: dict
    targets: list[dict]

    skill: Optional[dict] = None
    item: Optional[dict] = None

    data: Optional[Union[list, dict]] = None
    impacts: Optional[list[dict]] = None
    position: dict

    immediate: bool
    accepted: bool
    performed: bool
