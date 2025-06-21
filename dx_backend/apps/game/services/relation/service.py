from apps.character.models import Organization
from apps.core.models import BehaviorModel
from apps.game.services.character.core import CharacterService


class OrganizationRelationService:
    """
    The OrganizationRelationService is used to define and manage relationships between organizations.

    1. By default, the organization does not have any relations.
    2. When an organization faces another organization (organization.position == other_organization.position)
      - Checking if organization and other_organization have relations.
      - If no relations are found, then checking the other_organization default behavior and creating a relation if needed.
      - On organization relations change, change computes and changes character relations.
      - this must be possible that organization relation is BehaviorModel.PASSIVE or BehaviorModel.FRIENDLY but character relation is BehaviorModel.AGGRESSIVE and vice versa.
    """

    def __init__(self, organization: "Organization"):
        self.character = organization

    def acquire_organization_relation(self, other_organization: "Organization") -> BehaviorModel:
        """
        0. If the organization relation is immutable, then return the relation type without any checks.
        1. Check if the organization has relation with other_organization if none or not aggressive, then:
        2. Check if other_organization default behavior is aggressive, if so, then:
        3. Check the action log for aggressive actions against other_organization, if found, then: Aggressive
        """
        # Logic to acquire organization relation
        pass

    def recalculate_organization_relations(self, organization: "Organization") -> BehaviorModel:
        """
        Recalculate organization relations based on all existing org relations + treat all members that deos not haver relation as passive.
        This method should be called when a character relation changes.
        """
        # Logic to recalculate organization relations based on character relations
        pass


class CharacterRelationService:
    """
    The CharacterRelationService is used to define and manage relationships between characters and thar organizations.

    1. By default, the character does not have any relations.
    2. By default, the organization does not have any relations.
    3. When a character faced another character (character.position == other_character.position)
      - Checking if organization of character and other_character has relations.
      - Checking if character and other_character have relations.
      - If no relations are found, then checking the other_character default behavior and creating a relation if needed.
      - On character relations change, change computes and changes organization relations.
      - This must be possible that organization relation is BehaviorModel.PASSIVE or BehaviorModel.FRIENDLY but character relation is BehaviorModel.AGGRESSIVE and vice versa.
      - This must be possible that character1 to character2 relation is BehaviorModel.PASSIVE or BehaviorModel.FRIENDLY but character2 to character1 relation is BehaviorModel.AGGRESSIVE or vice versa.
    """

    def __init__(self, character: "CharacterService", org_relation_svc: OrganizationRelationService):
        self.character = character
        self.organization_relation_service = org_relation_svc

    def acquire_character_relation(self, other_character: "CharacterService") -> BehaviorModel:
        """
        1. Check if a character has a relation with other_character if none or not aggressive, then:
        2. Check if the organization of character has relation with the organization of other_character if none or not aggressive, then:
        3. Check if other_character default behavior is aggressive, if so, then:
        4. Check the action log for aggressive actions against other_character, if found, then: Aggressive
        """

    def become_aggressive(self, other_character: "CharacterService") -> None:
        """
        1. Check if a character has a relation with other_character, if not, then: create an aggressive relation.
        2. Recalculate organization relations based on all character relations.
        """
        pass

    def become_friendly(self, other_character: "CharacterService") -> None:
        """
        1. Check if a character has a relation with other_character, if not, then: create a friendly relation.
        2. Recalculate organization relations based on all character relations.
        """
        pass

    def become_passive(self, other_character: "CharacterService") -> None:
        """
        1. Check if a character has a relation with other_character, if not, then: create passive relation.
        2. Recalculate organization relations based on all character relations.
        """
        pass
