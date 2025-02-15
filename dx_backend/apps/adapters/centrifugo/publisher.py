import logging

from apps.adapters.centrifugo.client import CentrifugoClient
from apps.adapters.centrifugo.serializer import JsonSerializer
from apps.core.bus.protocol import Sender
from apps.core.bus.protocol.serializer import EventSerializer
from apps.core.bus.base import GameEvent

WSS_CLIENT = CentrifugoClient()


class CentrifugoPublisher(Sender):
    client = WSS_CLIENT
    logger = logging.getLogger("apps.adapters.centrifugo.publisher")
    serializer: EventSerializer = JsonSerializer()

    def send(self, message: GameEvent, channel: str) -> None:
        self.logger.debug(f"Sending message {message.full_event_name} to {channel}")
        self.client.publish(channel, self.serializer(message))

    def broadcast(self, message: GameEvent, channels: list[str]) -> None:
        self.logger.debug(f"Broadcasting message {message.full_event_name} to {channels}")
        self.client.broadcast(channels, self.serializer(message))

CENTRIFUGO_PUBLISHER = CentrifugoPublisher()