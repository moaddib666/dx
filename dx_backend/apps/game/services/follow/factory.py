from apps.character.models import FollowRule
from apps.game.services.character.core import CharacterService
from apps.game.services.follow.service import FollowTheLeaderService
from apps.game.services.world.movemant import MovementService


class ChaseFollowFactory:

    def __init__(self, movement_service: "MovementService" = None):
        """
        Initialize the ChaseFollowFactory.
        This factory is responsible for creating follow rules for characters.
        """
        self.movement_service = movement_service or MovementService()

    def follow(self, character: "CharacterService", target: "CharacterService") -> "FollowTheLeaderService":
        """
        Create permanent follow rule for the character to follow the target.
        Useful for pets of friendly NPCs.
        """
        follow_rule = FollowRule.objects.create(
            character=character.character,
            target=target.character,
            is_permanent=True,
        )
        return self.from_rule(follow_rule)

    def chase(self, character: "CharacterService", target: "CharacterService") -> "FollowTheLeaderService":
        """
        Create a chase follow rule for the character to chase the target.
        Useful for pets of aggressive NPCs.
        """
        follow_rule = FollowRule.objects.create(
            character=character.character,
            target=target.character,
            is_permanent=False,
            cycles_left=5,
        )
        return self.from_rule(follow_rule)

    def from_rule(self, rule: FollowRule) -> "FollowTheLeaderService":
        """
        Create a follow rule from an existing FollowRule object.
        This is useful for reusing existing rules.
        """
        return FollowTheLeaderService(
            rule=rule,
            movement_service=self.movement_service
        )


_default_chase_follow_factory = ChaseFollowFactory()


def get_chase_follow_factory() -> ChaseFollowFactory:
    """
    Get the default ChaseFollowFactory instance.

    Returns:
        ChaseFollowFactory: The default factory instance.
    """
    return _default_chase_follow_factory
