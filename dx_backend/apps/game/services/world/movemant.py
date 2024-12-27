from django.db import models

from apps.character.models import Character
from apps.game.exceptions import GameException
from apps.world.models import Position, PositionConnection


class MovementService:
    class MovementError(GameException):
        pass

    def move(self, character: Character, position: Position):
        """
        Move the player to the given position.
        """
        self.validate_move(character, position)
        character.position = position
        character.save()

    def validate_move(self, character: Character, position: Position):
        """
        Validate if the move is possible.
        """
        if not character.position:
            raise self.MovementError("Character has no position set.")
        if character.position == position:
            raise self.MovementError("Character is already in this position.")

        # Check if the target position is reachable
        current_position = character.position

        # Look for active, unlocked, and public connections
        connection_exists = PositionConnection.objects.filter(
            models.Q(position_from=current_position, position_to=position) |
            models.Q(position_from=position, position_to=current_position),
            is_active=True,
            is_locked=False,
            is_public=True
        ).exists()

        if not connection_exists:
            raise self.MovementError(f"Position {position} is not reachable from {current_position}.")
