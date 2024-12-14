from apps.core.bus.base import GameEventData, FightEvent, ConsumedMixin
from apps.core.models import CurrentTurn, FullPlayerInfo


class PlayerExample1GameEventData(GameEventData):
    field1: str


class PlayerExample1GameEvent(ConsumedMixin, FightEvent):
    data: PlayerExample1GameEventData


class PlayerExample2GameEventData(GameEventData):
    field2: str


class PlayerExample2GameEvent(ConsumedMixin, FightEvent):
    data: PlayerExample2GameEventData
