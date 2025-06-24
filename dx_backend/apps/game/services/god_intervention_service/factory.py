import typing as t

from apps.action.models import CharacterAction, Cycle
from apps.core.models import GodIntervention

if t.TYPE_CHECKING:
    from apps.game.services.character.core import CharacterService


class GodInterventionsFactory:
    """
    Factory for creating god_intervention_service objects with different sizes and attributes.
    """

    @classmethod
    def create_intervention(cls, **kwargs) -> GodIntervention:
        return GodIntervention(**kwargs)

    @classmethod
    def crete_character_intervention(cls, initiator: "CharacterService", target: "CharacterService",
                                     intervention: "GodIntervention") -> CharacterAction:
        action = CharacterAction.objects.create(
            action_type=CharacterAction.ActionType.GOD_INTERVENTION,
            initiator=initiator.character,
            data=intervention.model_dump(),
            cycle=Cycle.objects.current(campaign=initiator.character.campaign),
            position=target.character.position,
        )
        action.targets.add(target.character)
        return action
