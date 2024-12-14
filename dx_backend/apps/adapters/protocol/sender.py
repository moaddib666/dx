from typing import Protocol

from apps.adapters.name_resolver import GroupsNameResolver
from apps.adapters.protocol.serializer import EventSerializer
from apps.core.bus.base import GameEvent


class Sender(Protocol):
    name_resolver: GroupsNameResolver
    serializer: EventSerializer

    def send(self, message: GameEvent, channel: str) -> None:
        pass

    def broadcast(self, message: GameEvent, channels: list[str]) -> None:
        pass
