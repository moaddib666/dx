from apps.character.models import Organization, OrganizationRelation, CharacterRelation
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
        """
        # Check if there's an existing relation between the organizations
        try:
            relation = OrganizationRelation.objects.get(
                organization_from=self.character,
                organization_to=other_organization
            )

            # If the relation is immutable, return its type without any checks
            if relation.immutable:
                return relation.type

            return relation.type
        except OrganizationRelation.DoesNotExist:
            # If no relation exists, check the other organization's default behavior
            if other_organization.behavior == BehaviorModel.AGGRESSIVE:
                # Create an aggressive relation
                OrganizationRelation.objects.create(
                    organization_from=self.character,
                    organization_to=other_organization,
                    type=BehaviorModel.AGGRESSIVE
                )
                return BehaviorModel.AGGRESSIVE

            OrganizationRelation.objects.create(
                organization_from=self.character,
                organization_to=other_organization,
                type=BehaviorModel.PASSIVE
            )
            return BehaviorModel.PASSIVE

    def recalculate_organization_relations(self, organization: "Organization") -> BehaviorModel:
        """
        Recalculate organization relations based on all existing org relations + treat all members that deos not haver relation as passive.
        This method should be called when a character relation changes.
        """
        # Get all characters from both organizations
        from apps.character.models import Character

        our_characters = Character.objects.filter(organization=self.character)
        their_characters = Character.objects.filter(organization=organization)

        # Count the relations between characters
        aggressive_count = 0
        friendly_count = 0
        passive_count = 0

        for our_char in our_characters:
            for their_char in their_characters:
                try:
                    relation = CharacterRelation.objects.get(
                        character_from=our_char,
                        character_to=their_char
                    )
                    if relation.type == BehaviorModel.AGGRESSIVE:
                        aggressive_count += 1
                    elif relation.type == BehaviorModel.FRIENDLY:
                        friendly_count += 1
                    else:
                        passive_count += 1
                except CharacterRelation.DoesNotExist:
                    # If no relation exists, treat it as passive
                    passive_count += 1

        # Get or create the organization relation
        try:
            relation = OrganizationRelation.objects.get(
                organization_from=self.character,
                organization_to=organization
            )

            # If the relation is immutable, return its type without any changes
            if relation.immutable:
                return relation.type

            # Determine the new relation type based on character relations
            if aggressive_count > friendly_count and aggressive_count > passive_count:
                relation.type = BehaviorModel.AGGRESSIVE
            elif friendly_count > aggressive_count and friendly_count > passive_count:
                relation.type = BehaviorModel.FRIENDLY
            else:
                relation.type = BehaviorModel.PASSIVE

            relation.save()
            return relation.type

        except OrganizationRelation.DoesNotExist:
            # If no relation exists, create one based on character relations
            if aggressive_count > friendly_count and aggressive_count > passive_count:
                relation_type = BehaviorModel.AGGRESSIVE
            elif friendly_count > aggressive_count and friendly_count > passive_count:
                relation_type = BehaviorModel.FRIENDLY
            else:
                relation_type = BehaviorModel.PASSIVE

            OrganizationRelation.objects.create(
                organization_from=self.character,
                organization_to=organization,
                type=relation_type
            )
            return relation_type


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
        """
        # Check if there's an existing relation between the characters
        try:
            relation = CharacterRelation.objects.get(
                character_from=self.character.model,
                character_to=other_character.model
            )

            # If the relation is immutable, return its type without any checks
            if relation.immutable:
                return relation.type

            return relation.type
        except CharacterRelation.DoesNotExist:
            # If no relation exists, check the organization relations
            if self.character.model.organization and other_character.model.organization:
                # Get the organization relation service for the character's organization
                org_relation_service = self.organization_relation_service

                # Get the relation between the organizations
                org_relation_type = org_relation_service.acquire_organization_relation(other_character.model.organization)

                # If the organization relation is aggressive, create an aggressive character relation
                if org_relation_type == BehaviorModel.AGGRESSIVE:
                    CharacterRelation.objects.create(
                        character_from=self.character.model,
                        character_to=other_character.model,
                        type=BehaviorModel.AGGRESSIVE
                    )
                    return BehaviorModel.AGGRESSIVE

            # Check if the other character's default behavior is aggressive
            if other_character.model.behavior == BehaviorModel.AGGRESSIVE:
                CharacterRelation.objects.create(
                    character_from=self.character.model,
                    character_to=other_character.model,
                    type=BehaviorModel.AGGRESSIVE
                )
                return BehaviorModel.AGGRESSIVE

            CharacterRelation.objects.create(
                character_from=self.character.model,
                character_to=other_character.model,
                type=BehaviorModel.PASSIVE
            )
            return BehaviorModel.PASSIVE

    def become_aggressive(self, other_character: "CharacterService") -> None:
        """
        1. Check if a character has a relation with other_character, if not, then: create an aggressive relation.
        2. Recalculate organization relations based on all character relations.
        """
        # Check if there's an existing relation between the characters
        try:
            relation = CharacterRelation.objects.get(
                character_from=self.character.model,
                character_to=other_character.model
            )

            # If the relation is immutable, we can't change it
            if relation.immutable:
                return

            # Update the relation to be aggressive
            relation.type = BehaviorModel.AGGRESSIVE
            relation.save()
        except CharacterRelation.DoesNotExist:
            # If no relation exists, create an aggressive relation
            CharacterRelation.objects.create(
                character_from=self.character.model,
                character_to=other_character.model,
                type=BehaviorModel.AGGRESSIVE
            )

        # Recalculate organization relations if both characters belong to organizations
        if self.character.model.organization and other_character.model.organization:
            self.organization_relation_service.recalculate_organization_relations(other_character.model.organization)

    def become_friendly(self, other_character: "CharacterService") -> None:
        """
        1. Check if a character has a relation with other_character, if not, then: create a friendly relation.
        2. Recalculate organization relations based on all character relations.
        """
        # Check if there's an existing relation between the characters
        try:
            relation = CharacterRelation.objects.get(
                character_from=self.character.model,
                character_to=other_character.model
            )

            # If the relation is immutable, we can't change it
            if relation.immutable:
                return

            # Update the relation to be friendly
            relation.type = BehaviorModel.FRIENDLY
            relation.save()
        except CharacterRelation.DoesNotExist:
            # If no relation exists, create a friendly relation
            CharacterRelation.objects.create(
                character_from=self.character.model,
                character_to=other_character.model,
                type=BehaviorModel.FRIENDLY
            )

        # Recalculate organization relations if both characters belong to organizations
        if self.character.model.organization and other_character.model.organization:
            self.organization_relation_service.recalculate_organization_relations(other_character.model.organization)

    def become_passive(self, other_character: "CharacterService") -> None:
        """
        1. Check if a character has a relation with other_character, if not, then: create passive relation.
        2. Recalculate organization relations based on all character relations.
        """
        # Check if there's an existing relation between the characters
        try:
            relation = CharacterRelation.objects.get(
                character_from=self.character.model,
                character_to=other_character.model
            )

            # If the relation is immutable, we can't change it
            if relation.immutable:
                return

            # Update the relation to be passive
            relation.type = BehaviorModel.PASSIVE
            relation.save()
        except CharacterRelation.DoesNotExist:
            # If no relation exists, create a passive relation
            CharacterRelation.objects.create(
                character_from=self.character.model,
                character_to=other_character.model,
                type=BehaviorModel.PASSIVE
            )

        # Recalculate organization relations if both characters belong to organizations
        if self.character.model.organization and other_character.model.organization:
            self.organization_relation_service.recalculate_organization_relations(other_character.model.organization)
