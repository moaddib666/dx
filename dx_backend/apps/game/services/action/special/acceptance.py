import abc

from apps.action.models import SpecialAction
from apps.core.models import CharacterSpecialActionType
from apps.game.exceptions import GameException
from apps.game.services.character.core import CharacterService


class SpecialActionAcceptance:

    def __init__(self, action: SpecialAction):
        self.action = action

    def is_acceptable(self, initiator: CharacterService) -> bool:
        """
        Character has enough AP to perform snatch item
        Character is not dead
        Character is in safe location
        """
        try:
            self.check_acceptance(initiator)
            return True
        except GameException:
            return False

    @abc.abstractmethod
    def check_acceptance(self, initiator: CharacterService):
        pass


class DefaultSpecialActionAcceptance(SpecialActionAcceptance):

    def check_acceptance(self, initiator: CharacterService):
        """
        Character has enough AP to perform snatch item
        Character is not dead
        Character is in safe location
        """
        if initiator.get_current_ap() < self.action.ap_cost:
            raise GameException("Not enough action points")
        if initiator.get_current_hp() < 1:
            raise GameException("Character is dead")


class LongRestAcceptance(SpecialActionAcceptance):

    def is_acceptable(self, initiator: CharacterService) -> bool:
        """
        Character has enough AP to perform long rest
        Character is not dead
        Character is in safe location
        """
        try:
            self.check_acceptance(initiator)
            return True
        except GameException:
            return False

    def check_acceptance(self, initiator: CharacterService):
        if initiator.get_current_ap() < 1:
            raise GameException("Not enough action points")
        if initiator.get_current_hp() < 1:
            raise GameException("Character is dead")

        # character must be in a safe place to rest
        if not initiator.is_in_safe_place():
            raise GameException("Character is not in a safe place")


# SNATCH_ITEM

class SnatchItemAcceptance(SpecialActionAcceptance):
    def check_acceptance(self, initiator: CharacterService):
        """
        Character has enough AP to perform snatch item
        Character is not dead
        Character sees anybody in the same location
        """
        if initiator.get_current_ap() < 1:
            raise GameException("Not enough action points")
        if initiator.get_current_hp() < 1:
            raise GameException("Character is dead")
        if not initiator.not_alone():
            raise GameException("Nobody to snatch item from")


class BargainAcceptance(SpecialActionAcceptance):
    def check_acceptance(self, initiator: CharacterService):
        """
        Character has enough AP to perform snatch item
        Character is not dead
        Character sees anybody in the same location
        """
        if initiator.get_current_ap() < 1:
            raise GameException("Not enough action points")
        if initiator.get_current_hp() < 1:
            raise GameException("Character is dead")
        if not initiator.not_alone():
            raise GameException("Nobody to bargain with")


class InspectionAcceptance(SpecialActionAcceptance):
    def check_acceptance(self, initiator: CharacterService):
        """
        Character has enough AP to perform inspection
        Character is not dead
        Character sees anybody in the same location
        """
        if initiator.get_current_ap() < 1:
            raise GameException("Not enough action points")
        if initiator.get_current_hp() < 1:
            raise GameException("Character is dead")
        if not initiator.not_alone():
            raise GameException("Nobody to inspect")


class BackToSafeAcceptance(SpecialActionAcceptance):
    def check_acceptance(self, initiator: CharacterService):
        """
        Character has enough AP to perform back to safe
        Character is not dead
        Character is not in safe location
        """
        if initiator.get_current_ap() < 1:
            raise GameException("Not enough action points")
        if initiator.get_current_hp() < 1:
            raise GameException("Character is dead")
        if initiator.is_in_safe_place():
            raise GameException("Character is in a safe place already")


class AcceptanceFactory:
    # TODO: make autoregister via initsublass and add actiontype to abc
    mapping = {
        CharacterSpecialActionType.LONG_REST: LongRestAcceptance,
        CharacterSpecialActionType.SNATCH: SnatchItemAcceptance,
        CharacterSpecialActionType.BARGAIN: BargainAcceptance,
        CharacterSpecialActionType.GIFT: BargainAcceptance,
        CharacterSpecialActionType.INSPECT: InspectionAcceptance,
        CharacterSpecialActionType.BACK_TO_SAFE_ZONE: BackToSafeAcceptance,
    }
    default = DefaultSpecialActionAcceptance

    def from_action(self, action: SpecialAction) -> SpecialActionAcceptance:
        return self.mapping.get(action.action_type, self.default)(action)
