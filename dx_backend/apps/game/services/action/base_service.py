import abc

from apps.action.models import PlayerAction
from apps.game.services.player.core import PlayerService


class BaseService(abc.ABC):
    action: PlayerAction
    initiator: PlayerService
    target: list[PlayerService]

    def __init__(self, action: PlayerAction, initiator: PlayerService, targets: list[PlayerService]):
        self.action = action
        self.initiator = initiator
        self.target = targets

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

    @abc.abstractmethod
    def check(self):
        raise NotImplementedError
