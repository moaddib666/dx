import logging
import typing
from typing import Type

if typing.TYPE_CHECKING:
    from ..base import GameEvent


class EventsRegistry:
    produced: set[Type["GameEvent"]]
    consumed: set[Type["GameEvent"]]
    logger = logging.getLogger("apps.core.bus.registry")

    def __init__(self):
        self.produced = set()
        self.consumed = set()

    def register_produced(self, event: Type["GameEvent"]):
        self.logger.debug(f"Registering event {event} as produced")
        self.produced.add(event)

    def register_consumed(self, event: Type["GameEvent"]):
        self.logger.debug(f"Registering event {event} as consumed")
        self.consumed.add(event)

    def register(self, event: Type["GameEvent"]):
        self.register_produced(event)
        self.register_consumed(event)

    def auto_discover(self, events_module: str = "apps.core.bus.events"):
        # automatically recursivly import all modules in the events directory
        # and register all events in the module
        pass

    def get_all_events(self) -> set[Type["GameEvent"]]:
        return self.produced.union(self.consumed)


DEFAULT_EVENT_REGISTRY = EventsRegistry()
