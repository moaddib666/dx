from apps.action.models import CharacterAction, SpecialAction
from apps.game.exceptions import GameException
from apps.game.services.action.base_service import CharacterActionServicePrototype
from apps.game.services.bargain.gift_item import default_bargain_svc_factory
from apps.game.services.character.core import CharacterService
from apps.game.services.cost import DefaultCostService


class CharacterBargainService(CharacterActionServicePrototype):
    character_svc_cls = CharacterService
    cost_svc = DefaultCostService
    factory = default_bargain_svc_factory

    def perform(self, action: CharacterAction):
        # if targets > 1, raise exception
        if action.targets.count() > 1:
            raise GameException("Only one target is allowed")
        target = action.targets.first()
        # FIXME: when websocket is implemented, this should be changed to true bargain not just gift
        bargain = self.factory.gift_item_from_character(action.initiator, target)
        # Dirty hack
        action.data = {"bargain_id": str(bargain.model.id)}
        action.save(update_fields=["data"])

    def check(self, action: CharacterAction):
        char_svc = self.character_svc_cls(action.initiator)
        if char_svc.is_knocked_out():
            raise GameException("Character is knocked out")

    def check_acceptance(self, action: CharacterAction):
        # Character must have action points to move at least 1 point

        # TODO: reuse special action acceptance
        char_svc = self.character_svc_cls(action.initiator)
        if char_svc.get_current_ap() < 1:
            raise GameException("Not enough action points")
        if char_svc.get_current_hp() < 1:
            raise GameException("Character is dead")

        special_action = SpecialAction.objects.get(pk=action.action_type)
        self.cost_svc.validate(special_action.cost, char_svc)

    def accept(self, action: CharacterAction):
        # TODO: FIXME create special ActionClass and move reusable for special actions
        char_svc = self.character_svc_cls(action.initiator)
        special_action = SpecialAction.objects.get(pk=action.action_type)
        self.cost_svc.spend(special_action.cost, char_svc)
        action.immediate = special_action.immediate
        if special_action.final:
            char_svc.spend_all_ap()
        action.save(update_fields=["immediate"])


class CharacterGiftService(CharacterBargainService):
    def perform(self, action: CharacterAction):
        # if targets > 1, raise exception
        if action.targets.count() > 1:
            raise GameException("Only one target is allowed")
        target = action.targets.first()
        # FIXME: when websocket is implemented, this should be changed to true bargain not just gift
        bargain = self.factory.gift_item_from_character(action.initiator, target)
        # Dirty hack
        action.data = {"bargain_id": str(bargain.model.id)}
        action.save(update_fields=["data"])
