from apps.action.models import Cycle
from apps.core.bus import EventBusProto
from apps.core.bus.base import GameEvent, GameEventData, EventCategory
from apps.core.bus.events.world import NewCycleData


class BaseNotifier:
    def __init__(self, bus: EventBusProto):
        self.bus = bus

    def new_cycle(self, cycle: Cycle):
        event = GameEvent.create(
            name="new_cycle",
            category=EventCategory.WORLD,
            data=NewCycleData(id=cycle.id),
        )
        self.bus.publish(event)


