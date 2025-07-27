import uuid

from apps.core.bus.base import GameEventData, FightEvent, ProducedMixin


# Fight State Events

class FightStartedEventData(GameEventData):
    fight_id: uuid.UUID
    position_id: uuid.UUID
    attacker_id: uuid.UUID
    defender_id: uuid.UUID


class FightStartedEvent(ProducedMixin, FightEvent):
    data: FightStartedEventData
    name: str = "fight_started"

    @classmethod
    def create_event(cls, fight_id: uuid.UUID, position_id: uuid.UUID, attacker_id: uuid.UUID,
                     defender_id: uuid.UUID) -> "FightStartedEvent":
        return cls(
            data=FightStartedEventData(
                fight_id=fight_id,
                position_id=position_id,
                attacker_id=attacker_id,
                defender_id=defender_id,
            )
        )


class FightEndedEventData(GameEventData):
    fight_id: uuid.UUID
    position_id: uuid.UUID
    cycle_id: int


class FightEndedEvent(ProducedMixin, FightEvent):
    data: FightEndedEventData
    name: str = "fight_ended"

    @classmethod
    def create_event(cls, fight_id: uuid.UUID, position_id: uuid.UUID, cycle_id: int) -> "FightEndedEvent":
        return cls(
            data=FightEndedEventData(
                fight_id=fight_id,
                position_id=position_id,
                cycle_id=cycle_id,
            )
        )


# Character Join Events

class CharacterPendingJoinFightEventData(GameEventData):
    fight_id: uuid.UUID
    character_id: uuid.UUID
    position_id: uuid.UUID


class CharacterPendingJoinFightEvent(ProducedMixin, FightEvent):
    data: CharacterPendingJoinFightEventData
    name: str = "character_pending_join_fight"

    @classmethod
    def create_event(cls, fight_id: uuid.UUID, character_id: uuid.UUID,
                     position_id: uuid.UUID) -> "CharacterPendingJoinFightEvent":
        return cls(
            data=CharacterPendingJoinFightEventData(
                fight_id=fight_id,
                character_id=character_id,
                position_id=position_id,
            )
        )


class PendingJoinFightEventData(GameEventData):
    fight_id: uuid.UUID
    character_id: uuid.UUID


class PendingJoinFightEvent(ProducedMixin, FightEvent):
    data: PendingJoinFightEventData
    name: str = "pending_join_fight"

    @classmethod
    def create_event(cls, fight_id: uuid.UUID, character_id: uuid.UUID) -> "PendingJoinFightEvent":
        return cls(
            data=PendingJoinFightEventData(
                fight_id=fight_id,
                character_id=character_id,
            )
        )


class CharacterJoinFightEventData(GameEventData):
    fight_id: uuid.UUID
    character_id: uuid.UUID
    position_id: uuid.UUID


class CharacterJoinFightEvent(ProducedMixin, FightEvent):
    data: CharacterJoinFightEventData
    name: str = "character_join_fight"

    @classmethod
    def create_event(cls, fight_id: uuid.UUID, character_id: uuid.UUID,
                     position_id: uuid.UUID) -> "CharacterJoinFightEvent":
        return cls(
            data=CharacterJoinFightEventData(
                fight_id=fight_id,
                character_id=character_id,
                position_id=position_id,
            )
        )


class JoinedFightEventData(GameEventData):
    fight_id: uuid.UUID
    character_id: uuid.UUID


class JoinedFightEvent(ProducedMixin, FightEvent):
    data: JoinedFightEventData
    name: str = "joined_fight"

    @classmethod
    def create_event(cls, fight_id: uuid.UUID, character_id: uuid.UUID) -> "JoinedFightEvent":
        return cls(
            data=JoinedFightEventData(
                fight_id=fight_id,
                character_id=character_id,
            )
        )


# Character Leave Events

class CharacterLeaveFightEventData(GameEventData):
    fight_id: uuid.UUID
    character_id: uuid.UUID
    position_id: uuid.UUID


class CharacterLeaveFightEvent(ProducedMixin, FightEvent):
    data: CharacterLeaveFightEventData
    name: str = "character_leave_fight"

    @classmethod
    def create_event(cls, fight_id: uuid.UUID, character_id: uuid.UUID,
                     position_id: uuid.UUID) -> "CharacterLeaveFightEvent":
        return cls(
            data=CharacterLeaveFightEventData(
                fight_id=fight_id,
                character_id=character_id,
                position_id=position_id,
            )
        )


class LeftFightEventData(GameEventData):
    fight_id: uuid.UUID
    character_id: uuid.UUID


class LeftFightEvent(ProducedMixin, FightEvent):
    data: LeftFightEventData
    name: str = "left_fight"

    @classmethod
    def create_event(cls, fight_id: uuid.UUID, character_id: uuid.UUID) -> "LeftFightEvent":
        return cls(
            data=LeftFightEventData(
                fight_id=fight_id,
                character_id=character_id,
            )
        )
