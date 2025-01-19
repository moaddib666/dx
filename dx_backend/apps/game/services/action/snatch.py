import json

from apps.action.models import CharacterAction, SpecialAction
from apps.core.models import MultipleSnatchResult
from apps.game.exceptions import GameException
from apps.game.services.action.base_service import CharacterActionServicePrototype
from apps.game.services.character.character_behavior import CharacterBehaviorService
from apps.game.services.character.core import CharacterService
from apps.game.services.character.snatch import default_snatcher
from apps.game.services.cost import DefaultCostService


class CharacterSnatchActionService(CharacterActionServicePrototype):
    character_svc_cls = CharacterService
    snatcher = default_snatcher
    cost_svc = DefaultCostService

    def perform(self, action: CharacterAction):
        results = []
        for target in action.targets.all():
            result = self.snatcher.snatch(
                action.initiator,
                target,
            )
            CharacterBehaviorService(target).make_aggressive()
            results.append(result)
        action.data = json.loads(MultipleSnatchResult(targets=results).model_dump_json())
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
