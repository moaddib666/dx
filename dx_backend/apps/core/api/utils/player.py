from typing import TYPE_CHECKING

from rest_framework import viewsets

if TYPE_CHECKING:
    from apps.player.models import Player


from apps.game.exceptions import GameLogicException, GameException


class GenericGameViewSet(viewsets.GenericViewSet):

    def get_player(self) -> "Player":
        if not hasattr(self.request, 'user'):
            raise GameException('User not found in request')
        if not hasattr(self.request.user, 'player'):
            raise GameException('Player not found in request user')
        player = self.request.user.player
        if not player:
            raise GameLogicException('Player not found in request user')
        return player
