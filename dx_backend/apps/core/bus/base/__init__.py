import time
import uuid
from enum import StrEnum
from inspect import isabstract
from typing import Optional, Union

from pydantic import BaseModel, Field

from ..registry import EventsRegistry, DEFAULT_EVENT_REGISTRY


class GameEventData(BaseModel):

    class Config:
        from_attributes = True


class EventCategory(StrEnum):
    PLAYER = "character"
    LOCATION = "location"
    FIGHT = "fight"
    GAME = "game"
    WORLD = "world"


class EventDirection(StrEnum):
    PRODUCED = "character"
    CONSUMED = "server"


class GameEvent(BaseModel):
    name: str
    timestamp: int = Field(default_factory=lambda: int(time.time()))
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    category: EventCategory = EventCategory.GAME
    data: Optional[Union[list, dict]]

    __produced__: bool = False
    __consumed__: bool = False
    ___registry___: EventsRegistry = DEFAULT_EVENT_REGISTRY

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if isabstract(cls):
            return

        if cls.is_consumed():
            cls.___registry___.register_consumed(cls)
        if cls.is_produced():
            cls.___registry___.register_produced(cls)

    @classmethod
    def is_produced(cls) -> bool:
        return cls.__produced__

    @classmethod
    def is_consumed(cls) -> bool:
        return cls.__consumed__

    @property
    def full_event_name(self) -> str:
        return f"{self.category}.{self.name}"

    @classmethod
    def create(cls, category: EventCategory, name: str, data: GameEventData) -> "GameEvent":
        return cls(
            id=uuid.uuid4(),
            timestamp=int(time.time()),
            category=category,
            name=name,
            data=data.model_dump(),
        )


class ProducedMixin:
    __produced__ = True


class ConsumedMixin:
    __consumed__ = True


class FightEvent(GameEvent):
    category: EventCategory = EventCategory.FIGHT


class CharacterEvent(GameEvent):
    category: EventCategory = EventCategory.PLAYER


class LocationEvent(GameEvent):
    category: EventCategory = EventCategory.LOCATION
