import abc

from apps.action.models import CharacterAction
from apps.game.exceptions import GameException
from apps.game.services.character.core import CharacterService
from apps.game.services.world.movemant import MovementService


class BaseService(abc.ABC):
    """
    DESCRIPTION: This is used before and been deprecated
    """
    action: CharacterAction
    initiator: CharacterService
    target: list[CharacterService]
    movement: MovementService

    def __init__(self, action: CharacterAction, initiator: CharacterService, targets: list[CharacterService],
                 movement: MovementService):
        self.action = action
        self.initiator = initiator
        self.target = targets

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

    @abc.abstractmethod
    def check(self):
        raise NotImplementedError


class CharacterActionServicePrototype(abc.ABC):

    @abc.abstractmethod
    def perform(self, action: CharacterAction):
        raise GameException("Not implemented")

    @abc.abstractmethod
    def check(self, action: CharacterAction):
        """Check if the action is possible to perform"""
        raise GameException("Not implemented")

    @abc.abstractmethod
    def check_acceptance(self, action: CharacterAction):
        """Check if the action is possible to accept"""
        raise GameException("Not implemented")

    @abc.abstractmethod
    def accept(self, action: CharacterAction):
        """Accept the action making it possible to perform it raise GameException if not possible"""
        raise GameException("Not implemented")


class CharacterActionPlayerServicePrototype(abc.ABC):

    @abc.abstractmethod
    def prepare(self):
        raise GameException("Not implemented")

    @abc.abstractmethod
    def play(self):
        raise GameException("Not implemented")
