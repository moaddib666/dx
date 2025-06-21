from apps.action.models import CharacterAction
from apps.core.models import GodIntervention
from apps.game.exceptions import GameLogicException
from apps.game.services.action.base_service import SingleTargetActionServicePrototype
from apps.game.services.character.core import CharacterService
from apps.game.services.effect.assigner import DefaultEffectManager
from apps.game.services.god_intervention_service.base import GodInterventionService


class CharacterGodInterventionActionService(SingleTargetActionServicePrototype):
    """
    Service for handling god_intervention_service actions on characters.
    """
    character_svc_cls = CharacterService
    intervention_svc_cls = GodInterventionService
    effect_assign_svc = DefaultEffectManager

    @staticmethod
    def get_intervention(action: CharacterAction) -> GodIntervention:
        return GodIntervention(**action.data)

    def perform(self, action: CharacterAction):
        """
        Perform the god_intervention_service action on the target character.
        """
        intervention = self.get_intervention(action)
        character_svc = self.get_target(action)
        # Apply the god_intervention_service
        intervention_svc = self.intervention_svc_cls(character_svc)
        effects_svc = self.effect_assign_svc()
        # Remove all exiting effects before applying the god_intervention_service
        effects_svc.remove_all(character_svc)
        # Calculating impacts from the god_intervention_service
        impacts = intervention_svc.act(intervention)
        # Register the impacts to log the action
        self.register_impacts(action, impacts)

    def check(self, action: CharacterAction):
        """
        Check if the god_intervention_service action can be performed.
        
        Args:
            action: The god_intervention_service action to check
        """
        character_svc = self.get_target(action)
        intervention = self.get_intervention(action)
        if intervention.type.is_curse():
            if character_svc.is_knocked_out():
                raise GameLogicException("Cannot apply curse to a character that is not knocked out")
        return True

    def check_acceptance(self, action: CharacterAction):
        """
        GM - Action Always can be accepted.
        """
        return True

    def accept(self, action: CharacterAction):
        """
        God Intervention actions are always accepted immediately.
        """
        action.immediate = True
        action.save()
        return True
