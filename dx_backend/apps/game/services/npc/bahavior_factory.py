from functools import partial

from apps.character.models import Character
from apps.core.models import BehaviorModel
from apps.game.exceptions import GameException
from apps.game.services.npc.aggresive_behavior import AggressiveBehaviorService
import typing as t

from apps.game.services.npc.friendly_behavior import FriendlyBehaviorService

if t.TYPE_CHECKING:
    from apps.game.services.action.accept import ActionAcceptor


class BehaviorFactory:
    class MissingBehavior(GameException):
        pass

    def __init__(self, actions_acceptor: partial["ActionAcceptor"]) -> None:
        self.behaviors = {
            BehaviorModel.AGGRESSIVE: AggressiveBehaviorService,
            BehaviorModel.FRIENDLY: FriendlyBehaviorService,
        }
        self.actions_acceptor = actions_acceptor

    def get(self, char: Character) -> AggressiveBehaviorService:
        try:
            return self.behaviors[char.behavior](char, self.actions_acceptor)
        except KeyError:
            raise self.MissingBehavior(f"Behavior {char.behavior} not implemented")
