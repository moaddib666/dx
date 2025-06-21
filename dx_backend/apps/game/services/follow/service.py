from apps.character.models import FollowRule
from apps.core.models import MoveTypes
from apps.game.exceptions import GameException
from apps.game.services.character.core import CharacterService
from apps.game.services.world.movemant import MovementService


class FollowTheLeaderService:
    def __init__(self, rule: "FollowRule", movement_service: "MovementService"):
        self.rule = rule
        self.leader = CharacterService(rule.leader)
        self.follower = CharacterService(rule.follower)
        self.movement_service = movement_service

    def should_proceed(self) -> bool:
        """
        Check if the follower should continue following the leader.
        This method can be used to determine if the follower should keep moving.

        Returns:
            bool: True if the follower should proceed, False otherwise.
        """
        if self.follower.is_knocked_out():
            return False
        if self.rule.permanent:
            return True
        if self.rule.cycles_left <= 0:
            return False
        return True

    def move(self):
        """
        Move the follower towards the leader.
        This method should be called periodically to update the follower's position.
        """
        if self.rule.type != MoveTypes.TELEPORT:
            raise GameException("Not implemented yet")

        self.movement_service.teleport(
            character=self.follower.character,
            position=self.leader.character.position
        )


