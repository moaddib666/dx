from typing import TYPE_CHECKING

from rest_framework import viewsets

if TYPE_CHECKING:
    from apps.character.models import Character


from apps.game.exceptions import GameLogicException, GameException


class GenericGameViewSet(viewsets.GenericViewSet):

    def get_character(self) -> "Character":
        if not hasattr(self.request, 'user'):
            raise GameException('User not found in request')
        if not hasattr(self.request.user, 'main_character'):
            raise GameException('Character not found in request user')
        character = self.request.user.main_character
        if not character:
            raise GameLogicException('Character not found in request user')
        return character
