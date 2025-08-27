import uuid

from apps.core.bus.base import GameEventData, CharacterEvent, ProducedMixin


class ChallengeCreatedEventData(GameEventData):
    """Data for challenge created event with full typing coverage."""
    id: uuid.UUID
    character_id: uuid.UUID


class ChallengeCreatedEvent(ProducedMixin, CharacterEvent):
    """Event fired when a new challenge is created for a character."""
    data: ChallengeCreatedEventData
    name: str = "challenge_created"

    @classmethod
    def create_event(cls, id: uuid.UUID, character_id: uuid.UUID) -> "ChallengeCreatedEvent":
        return cls(
            data=ChallengeCreatedEventData(
                id=id,
                character_id=character_id,
            )
        )
