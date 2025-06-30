import logging

from django.db import models

from apps.character.models import Character
from apps.core.models import BehaviorModel, CharacterStats
from apps.game.exceptions import GameException
from apps.game.services.character.core import CharacterService
from apps.game.services.world.position_connection import PositionConnectionService
from apps.world.models import Position, PositionConnection


class MovementService:
    logger = logging.getLogger("game.services.world.movement")

    class MovementError(GameException):
        pass

    def teleport(self, character: Character, position: Position):
        """
        Teleport the player to the given position.
        """
        if not position:
            raise self.MovementError("Position cannot be None.")
        if not character.position:
            raise self.MovementError("Character has no position set.")
        if character.position == position:
            return

        character.position = position
        character.save(
            update_fields=["position", "updated_at"]
        )

    def move(self, character: Character, position: Position):
        """
        Move the player to the given position.
        """
        self.validate_move(character, position, include_npc=True)
        character.position = position
        character.save(
            update_fields=["position", "updated_at"]
        )

    def validate_move(self, character: Character, position: Position, include_npc=False):
        """
        Validate if the move is possible.
        """
        if not character.position:
            raise self.MovementError("Character has no position set.")
        if character.position == position:
            raise self.MovementError("Character is already in this position.")

        # Check if the target position is reachable
        current_position = character.position

        # Find the connection between the current position and the target position
        connection = PositionConnection.objects.filter(
            models.Q(position_from=current_position, position_to=position) |
            models.Q(position_from=position, position_to=current_position)
        ).first()

        if not connection:
            raise self.MovementError(f"Position {position} is not reachable from {current_position}.")

        # Create a CharacterService instance for the character
        char_svc = CharacterService(character)

        # Create a PositionConnectionService instance for the connection
        connection_svc = PositionConnectionService(connection)

        # Check if the connection is accessible for the character
        if not connection_svc.is_accessible(char_svc):
            raise self.MovementError(f"Position {position} is not accessible from {current_position}.")

        if include_npc:
            self.validate_other_requirements(character, position)

    def validate_other_requirements(self, character: Character, position: Position):
        """
        Validate other requirements for the move.

        For example, if the character is attacked by an aggressive NPC, the move is canceled.
        """

        current_position = character.position
        npc_chars = current_position.gameobject_set.instance_of(Character).filter(
            character__npc=True,
            character__is_active=True,
            character__behavior=BehaviorModel.AGGRESSIVE
        )
        char_svc = CharacterService(character)
        for npc_char in npc_chars:
            npc_char_svc = CharacterService(npc_char)
            dice_roll_char = char_svc.roll_dice(sides=20) + char_svc.get_stat(CharacterStats.SPEED)
            dice_roll_npc = npc_char_svc.roll_dice(sides=20) + npc_char_svc.get_stat(CharacterStats.SPEED)
            if dice_roll_char < dice_roll_npc:
                self.logger.debug(f"Character {character} was attacked by {npc_char} and the move was canceled.")
                raise self.MovementError(f"Character {character} was attacked by {npc_char} and the move was canceled.")
