import logging

from apps.action.models import Cycle, CharacterAction
from apps.core.bus import EventBusProto
from apps.core.bus.base import GameEvent, EventCategory
from apps.core.bus.events.world import NewCycleData, ActionAcceptedData
from apps.core.models import RegisteredImpact, RegisteredDiceRoll


class BaseNotifier:
    logger = logging.getLogger("game.services.notifier")

    def __init__(self, bus: EventBusProto):
        self.bus = bus

    def new_cycle(self, cycle: Cycle):
        event = GameEvent.create(
            name="new_cycle",
            category=EventCategory.WORLD,
            data=NewCycleData(id=cycle.id),
        )
        self.bus.publish(event)

    def _serialize_impact(self, imp) -> RegisteredImpact:
        return RegisteredImpact(
            id=imp.id,
            dice_roll_result=RegisteredDiceRoll(
                dice_side=imp.dice_roll_result.dice_side,
                outcome=imp.dice_roll_result.outcome,
            ) if imp.dice_roll_result else None,
            type=imp.type,
            violation=imp.violation,
            size=imp.size,
            target=imp.target.id,
        )

    def _serialize_action_to_accepted_data(self, action: CharacterAction) -> ActionAcceptedData:
        # Ugly import to avoid circular imports and looks like a hack
        from apps.action.api.serializers.openapi import GameMasterCharacterActionLogSerializer
        # get current request and add this to context of the serializer
        from dx_backend.middleware import get_current_request
        context = {
            "request": get_current_request()
        }
        return ActionAcceptedData(**GameMasterCharacterActionLogSerializer(action, context=context).data)

    def action_not_accepted(self, action: CharacterAction, exception: Exception):
        self.logger.warning(
            f"Action {action.id} not accepted with exception {exception}", exc_info=True
        )
        action_data = self._serialize_action_to_accepted_data(action)
        event = GameEvent.create(
            name="action_not_accepted",
            category=EventCategory.WORLD,
            data=action_data,
        )
        self.bus.publish(event)

    def action_accepted(self, action: CharacterAction):
        self.logger.debug(f"Action {action} accepted")
        action_data = self._serialize_action_to_accepted_data(action)
        event = GameEvent.create(
            name="action_accepted",
            category=EventCategory.WORLD,
            data=action_data,
        )
        self.bus.publish(event)

    def action_performed(self, action: CharacterAction):
        self.logger.debug(f"Action {action} performed")
        action_data = self._serialize_action_to_accepted_data(action)
        event = GameEvent.create(
            name="action_performed",
            category=EventCategory.WORLD,
            data=action_data,
        )
        self.bus.publish(event)

    def action_failed(self, action: CharacterAction, exception: Exception):
        self.logger.warning(
            f"Action {action.id} failed with exception {exception}", exc_info=True
        )
        action_data = self._serialize_action_to_accepted_data(action)
        event = GameEvent.create(
            name="action_failed",
            category=EventCategory.WORLD,
            data=action_data,
        )
        self.bus.publish(event)
