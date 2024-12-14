from apps.action.models import ActionImpact
from apps.adapters.centrifugo.publisher import CentrifugoPublisher
from apps.adapters.name_resolver import FightGroupsNameResolver
from apps.core.bus.base import GameEvent
from apps.core.bus.events import FightTurnActionResultGameEvent
from apps.core.models import ActionModel, ActionImpactModel
from apps.fight.models import FightTurnAction


class FightNotifier(CentrifugoPublisher):
    name_resolver: FightGroupsNameResolver = FightGroupsNameResolver()

    def __init__(self, fight_id: str):
        self.fight_id = fight_id

    def broadcast_fight(self, message: GameEvent):
        fight_group = self.name_resolver.construct_fight_group_name(self.fight_id)
        self.broadcast(message, [fight_group])

    def broadcast_fight_side(self, side: str, message: GameEvent):
        fight_side_group = self.name_resolver.construct_fight_side_group_name(self.fight_id, side)
        self.broadcast(message, [fight_side_group])

    def send_participant(self, participant: str, message: GameEvent):
        participant_group = self.name_resolver.construct_participant_group_name(self.fight_id, participant)
        self.broadcast(message, [participant_group])

    def send_action_result(self, action: FightTurnAction, impacts: list[ActionImpact]):
        self.logger.debug(f"Preparing to send action result {action} {impacts}")
        for impact in impacts:
            self.logger.info(f'Sending action result {action} {impact}')
            event = FightTurnActionResultGameEvent.create_event(
                turn_id=action.turn.id,
                initiator_id=action.initiator.id,
                target_id=impact.target.id,
                action=ActionModel.from_orm(action),
                impact=ActionImpactModel.from_orm(impact),
            )
            self.broadcast_fight(event)
