import logging
from typing import Protocol

from .base import GameEvent
from .channels import Channel
from .protocol import Sender


class EventBusProto(Protocol):

    def on_new_message(self, event: GameEvent):
        pass

    def subscribe(self, topic, callback):
        pass

    def publish(self, event: GameEvent):
        pass

    @classmethod
    def set_publisher(cls, publisher: Sender):
        pass


class _PubSub(EventBusProto):
    publisher: Sender
    logger = logging.getLogger("apps.core.bus.pubsub")

    def on_new_message(self, event: GameEvent):
        self.logger.debug(f"Received event {event}")
        pass

    def subscribe(self, topic, callback):
        self.logger.debug(f"Subscribing to {topic}")
        pass

    def publish(self, event: GameEvent):
        self.logger.debug(f"Publishing event {event}")
        self.publisher.send(event, Channel.WORLD)

    @classmethod
    def set_publisher(cls, publisher: Sender):
        cls.logger.debug(f"Setting publisher to {publisher}")
        cls.publisher = publisher


event_bus = _PubSub()


def setup_publisher(publisher: Sender):
    event_bus.set_publisher(publisher)
