import uuid

from apps.core.bus.base import GameEventData, FightEvent, ProducedMixin
from apps.core.models import CurrentTurn, FullPlayerInfo, ActionModel, ActionImpactModel


class PlayerNewTurnGameEventData(GameEventData):
    current_turn: CurrentTurn
    player_info: FullPlayerInfo


class PlayerNewTurnGameEvent(ProducedMixin, FightEvent):
    data: PlayerNewTurnGameEventData
    name: str = "player_turn_init"

    @classmethod
    def create_event(cls, current_turn: CurrentTurn, player_info: FullPlayerInfo) -> "PlayerNewTurnGameEvent":
        return cls(
            data=PlayerNewTurnGameEventData(
                current_turn=current_turn,
                player_info=player_info,
            )
        )


class TurnActionResultGameEventData(GameEventData):
    turn_id: uuid.UUID
    initiator_id: uuid.UUID
    target_id: uuid.UUID
    action: ActionModel
    impact: ActionImpactModel


class FightTurnActionResultGameEvent(ProducedMixin, FightEvent):
    data: TurnActionResultGameEventData
    name: str = "turn_result"

    @classmethod
    def create_event(cls, turn_id: uuid.UUID, initiator_id: uuid.UUID, target_id: uuid.UUID, action: ActionModel, impact: ActionImpactModel) -> "FightTurnActionResultGameEvent":
        return cls(
            data=TurnActionResultGameEventData(
                turn_id=turn_id,
                initiator_id=initiator_id,
                target_id=target_id,
                action=action,
                impact=impact,
            )
        )

