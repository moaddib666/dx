from apps.core.bus.base import GameEventData, FightEvent, ConsumedMixin
from apps.core.models import CurrentTurn, FullCharacterInfo


class CharacterExample1GameEventData(GameEventData):
    field1: str


class CharacterExample1GameEvent(ConsumedMixin, FightEvent):
    data: CharacterExample1GameEventData


class CharacterExample2GameEventData(GameEventData):
    field2: str


class CharacterExample2GameEvent(ConsumedMixin, FightEvent):
    data: CharacterExample2GameEventData
