from typing import Protocol

from apps.core.bus.base import GameEvent
from apps.core.bus.protocol.serializer import EventSerializer


class Sender(Protocol):
    serializer: EventSerializer

    def send(self, message: GameEvent, channel: str) -> None:
        pass

    def broadcast(self, message: GameEvent, channels: list[str]) -> None:
        pass
