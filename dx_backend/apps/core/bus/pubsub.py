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
        elif event.name == "challenge_created":
            # Send challenge_created event to specific character instead of broadcasting
            character_id = event.data.character_id
            if character_id:
                character_channel = Channel.character(character_id)
                self.publisher.send(event, character_channel)
                self.logger.debug(f"Sent challenge_created event to character channel: {character_channel}")
            else:
                self.logger.warning("ChallengeCreatedEvent missing character_id, sending to MASTER")
                self.publisher.send(event, Channel.MASTER)
        else:
            self.publisher.send(event, Channel.MASTER)

    @classmethod
    def set_publisher(cls, publisher: Sender):
        cls.logger.debug(f"Setting publisher to {publisher}")
        cls.publisher = publisher


event_bus = _PubSub()


def setup_publisher(publisher: Sender):
    event_bus.set_publisher(publisher)
