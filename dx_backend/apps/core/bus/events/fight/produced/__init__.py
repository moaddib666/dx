import uuid

from apps.core.bus.base import GameEventData, FightEvent, ProducedMixin
from apps.core.models import CurrentTurn, FullCharacterInfo, ActionModel, ActionImpactModel


class CharacterNewTurnGameEventData(GameEventData):
    current_turn: CurrentTurn
    character_info: FullCharacterInfo


class CharacterNewTurnGameEvent(ProducedMixin, FightEvent):
    data: CharacterNewTurnGameEventData
    name: str = "character_turn_init"

    @classmethod
    def create_event(cls, current_turn: CurrentTurn, character_info: FullCharacterInfo) -> "CharacterNewTurnGameEvent":
        return cls(
            data=CharacterNewTurnGameEventData(
                current_turn=current_turn,
                character_info=character_info,
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

