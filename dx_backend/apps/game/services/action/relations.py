from apps.action.models import CharacterAction
from apps.character.models import Character
from apps.game.services.character.core import CharacterService
from apps.game.services.relation.service import get_character_relation_service


class ActionRelationService:

    def __init__(self, action: "CharacterAction"):
        self.action = action

    def become_aggressive(self):
        """
        Make all action participants aggressive towards each other.
        """
        initiator = CharacterService(self.action.initiator)
        initiator_relation = get_character_relation_service(initiator)

        for target_character in self.action.targets.instance_of(Character):
            target = CharacterService(target_character)
            target_relation = get_character_relation_service(target)
            initiator_relation.become_aggressive_to(target)
            target_relation.become_aggressive_to(initiator)


class ActionRelationServiceFactory:

    @staticmethod
    def from_action(action: "CharacterAction") -> ActionRelationService:
        """
        Create an ActionRelationService from a CharacterAction instance.

        Args:
            action: The CharacterAction instance to create the service for.

        Returns:
            ActionRelationService: The service instance for the action.
        """
        return ActionRelationService(action)
