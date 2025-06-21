import abc
import typing as t
from abc import ABC

from apps.action.models import CharacterAction
from apps.action.models import DiceRollResult
from apps.game.exceptions import GameException
from apps.game.services.character.core import CharacterService
from apps.game.services.world.movemant import MovementService

if t.TYPE_CHECKING:
    from apps.action.models import ActionImpact, CharacterAction, DiceRollResult
    from apps.core.models import ActionImpactModel


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


class SingleTargetActionServicePrototype(CharacterActionServicePrototype, ABC):

    @staticmethod
    def register_impact(action: "CharacterAction", calculated_impact: "ActionImpactModel",
                        dice_roll_result: "DiceRollResult") -> "ActionImpact":
        """
        Register an impact from the god_intervention_service.

        Args:
            action: The god_intervention_service action
            calculated_impact: The impact to register
            dice_roll_result: The dice roll result for the impact
        """
        return action.impacts.create(
            target=action.targets.first(),
            type=calculated_impact.type,
            violation=calculated_impact.violation,
            size=calculated_impact.size,
            dice_roll_result=dice_roll_result
        )

    def register_impacts(self, action: "CharacterAction", calculated_impacts: t.List["ActionImpactModel"]) -> t.List[
        "ActionImpact"]:
        """
        Register multiple impacts from the action.

        Args:
            action: The action to register impacts for
            calculated_impacts: List of impacts to register

        Returns:
            List of registered action impacts
        """
        results = []
        for impact in calculated_impacts:
            dice_roll_result = DiceRollResult.objects.create(
                multiplier=impact.dice_roll_result.multiplier,
                dice_side=impact.dice_roll_result.dice_side,
                outcome=impact.dice_roll_result.outcome,
            )
            results.append(
                self.register_impact(action, impact, dice_roll_result)
            )
        return results

    @staticmethod
    def get_target(action: "CharacterAction") -> "CharacterService":
        """
        Get the target character from the action.

        Args:
            action: The action to get the target from

        Returns:
            The target character service instance
        """
        if not action.targets.exists():
            raise GameException("No target character specified for action")
        return CharacterService(action.targets.first())


class CharacterActionPlayerServicePrototype(abc.ABC):

    @abc.abstractmethod
    def prepare(self):
        raise GameException("Not implemented")

    @abc.abstractmethod
    def play(self):
        raise GameException("Not implemented")
