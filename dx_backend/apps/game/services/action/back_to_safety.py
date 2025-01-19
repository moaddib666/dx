from apps.action.models import CharacterAction, SpecialAction
from apps.game.exceptions import GameException
from apps.game.services.action.base_service import CharacterActionServicePrototype
from apps.game.services.character.core import CharacterService
from apps.game.services.cost import DefaultCostService
from apps.world.models import Position


class BackToSafeService(CharacterActionServicePrototype):
    cost_svc = DefaultCostService
    character_svc_cls = CharacterService

    def perform(self, action: CharacterAction):
        action.initiator.position = action.initiator.last_safe_position or Position.objects.get(
            grid_x=0, grid_y=1, grid_z=1,
        )
        action.initiator.save(
            update_fields=["position", "updated_at"]
        )

    def check(self, action: CharacterAction):
        char_svc = self.character_svc_cls(action.initiator)
        if char_svc.is_in_safe_place():
            raise GameException("Character is already in a safe place")
        if char_svc.is_knocked_out():
            raise GameException("Character is knocked out")

    def check_acceptance(self, action: CharacterAction):
        char_svc = self.character_svc_cls(action.initiator)
        if char_svc.is_knocked_out():
            raise GameException("Character is knocked out")
        # TODO: reuse special action acceptance
        special_action = SpecialAction.objects.get(pk=action.action_type)
        self.cost_svc.validate(special_action.cost, char_svc)

    def accept(self, action: CharacterAction):
        char_svc = self.character_svc_cls(action.initiator)
        # TODO: reuse special action acceptance
        special_action = SpecialAction.objects.get(pk=action.action_type)
        self.cost_svc.spend(special_action.cost, char_svc)
        char_svc.spend_all_ap()
