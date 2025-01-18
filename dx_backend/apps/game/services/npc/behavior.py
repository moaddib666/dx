import logging
import typing as t
from functools import partial

from apps.action.models import CharacterAction
from apps.character.models import Character

if t.TYPE_CHECKING:
    from ..action.accept import ActionAcceptor


class BehaviorServiceProtocol(t.Protocol):
    """
    Protocol for behavior services.
    """
    logger = logging.getLogger("game.service.npc.behavior")

    def __init__(self, character: Character, action_acceptor: partial["ActionAcceptor"]) -> None:
        self.character = character
        self.action_acceptor = action_acceptor

    def behave(self) -> None:
        ...

    def has_targets(self) -> bool:
        ...

    def need_energy(self) -> bool:
        ...

    def need_shield(self) -> bool:
        ...

    def need_heal(self) -> bool:
        ...

    def can_behave(self) -> bool:
        ...

    def get_potential_enemies(self) -> [Character]:
        ...

    def get_potential_friends(self) -> [Character]:
        ...

    def accept_action(self, action: 'CharacterAction') -> None:
        self.action_acceptor(action).accept()
