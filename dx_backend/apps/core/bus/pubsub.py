import logging
from typing import Protocol

from .base import GameEvent
from .channels import Channel
from .protocol import Sender


class EventBusProto(Protocol):

    def on_new_message(self, event: GameEvent):
        pass

    def subscribe(self, chanel, callback):
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

    def subscribe(self, chanel, callback):
        self.logger.debug(f"Subscribing to {chanel}")
        pass

    def publish(self, event: GameEvent):
        self.logger.debug(f"Publishing event {event}")
        # FIXME: add abstraction of target
        #  Where:
        #  - target Character
        #  - target Group
        #  - target Position
        #  - target Location
        #  - target World
        #  - target System
        #  - target GameMaster
        if event.name == "new_cycle":
            self.publisher.send(event, Channel.WORLD)
        self.publisher.send(event, Channel.MASTER)

    @classmethod
    def set_publisher(cls, publisher: Sender):
        cls.logger.debug(f"Setting publisher to {publisher}")
        cls.publisher = publisher


event_bus = _PubSub()


def setup_publisher(publisher: Sender):
    event_bus.set_publisher(publisher)
