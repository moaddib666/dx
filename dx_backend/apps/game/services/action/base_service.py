import abc

from apps.action.models import CharacterAction
from apps.game.services.character.core import CharacterService


class BaseService(abc.ABC):
    action: CharacterAction
    initiator: CharacterService
    target: list[CharacterService]

    def __init__(self, action: CharacterAction, initiator: CharacterService, targets: list[CharacterService]):
        self.action = action
        self.initiator = initiator
        self.target = targets

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

    @abc.abstractmethod
    def check(self):
        raise NotImplementedError
