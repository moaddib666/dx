from typing import Protocol, Any

from apps.core.bus.base import GameEvent


class EventSerializer(Protocol):

    def __call__(self, event: "GameEvent") -> Any:
        ...
