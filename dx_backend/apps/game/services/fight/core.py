import typing as t

from apps.fight.models import Fight

if t.TYPE_CHECKING:
    from apps.action.models import Cycle
    from apps.character.models import Character

# Import the refactored classes
from .detector import FightDetector
from .auto_joiner import FightAutoJoiner
from .auth_leaver import FightAuthLeaver
from .pending_joiner import FightPendingJoiner
from .fight_closer import FightCloser
from .coordinator import FightCoordinator


class FightFactory:
    """
    Factory for creating Fight instances.
    """
    model: t.Type[Fight] = Fight

    def create_fight(self, cycle: "Cycle", attacker: "Character", defender: "Character", position=None) -> Fight:
        """
        Creates a new fight instance with the given parameters.

        :param cycle: The current cycle in which the fight is happening.
        :param attacker: The character who initiated the fight.
        :param defender: The character who is being attacked.
        :param position: The position where the fight takes place (optional, 
                        will use attacker's position if not provided).
        :return: A new Fight instance.
        """
        if position is None:
            position = attacker.position

        return self.model.objects.create(
            created=cycle,
            attacker=attacker,
            defender=defender,
            position=position,
            open=True
        )


# Re-export the classes for backward compatibility
__all__ = [
    'FightFactory',
    'FightDetector',
    'FightAutoJoiner',
    'FightAuthLeaver',
    'FightPendingJoiner',
    'FightCloser',
    'FightCoordinator'
]
