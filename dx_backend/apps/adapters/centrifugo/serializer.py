from apps.core.bus.protocol.serializer import EventSerializer
from apps.core.bus.base import GameEvent


class JsonSerializer(EventSerializer):

    def __call__(self, event: GameEvent):
        return event.json()
