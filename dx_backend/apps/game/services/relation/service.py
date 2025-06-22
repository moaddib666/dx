from typing import Dict, Optional

from django.db import transaction
from django.db.models import Count

from apps.character.models import Organization, OrganizationRelation, CharacterRelation, Character
from apps.core.models import BehaviorModel
from apps.game.services.character.core import CharacterService


class RelationshipCalculator:
    """Utility class for relationship calculations and business logic."""

    @staticmethod
    def determine_relation_from_counts(aggressive: int, friendly: int, passive: int) -> BehaviorModel:
        """
        Determine relationship type based on counts using a more sophisticated algorithm.

        Args:
            aggressive: Count of aggressive relationships
            friendly: Count of friendly relationships  
            passive: Count of passive relationships

        Returns:
            The determined BehaviorModel type
        """
        total = aggressive + friendly + passive
        if total == 0:
            return BehaviorModel.PASSIVE

        # Calculate percentages for more nuanced decision making
        aggressive_pct = aggressive / total
        friendly_pct = friendly / total

        # Require a significant majority (>40%) to override passive default
        if aggressive_pct > 0.4 and aggressive > friendly:
            return BehaviorModel.AGGRESSIVE
        elif friendly_pct > 0.4 and friendly > aggressive:
            return BehaviorModel.FRIENDLY
        else:
            return BehaviorModel.PASSIVE


class OrganizationRelationService:
    """
    Service for managing relationships between organizations.

    This service handles:
    1. Acquiring/creating organization relationships based on default behaviors
    2. Recalculating organization relationships based on character relationships
    3. Ensuring relationship consistency and immutability rules
    """

    def __init__(self, organization: Organization):
        self.organization = organization

    def get_relation_to(self, target_organization: Organization) -> BehaviorModel:
        """
        Get the relationship type to another organization.
        Creates the relationship if it doesn't exist.

        Args:
            target_organization: The organization to get relationship with

        Returns:
            The relationship type (BehaviorModel)
        """
        if self.organization.id == target_organization.id:
            return BehaviorModel.PASSIVE  # Organization can't have relation with itself

        relation = self._get_existing_relation(target_organization)

        if relation:
            return relation.type

        return self._create_initial_relation(target_organization)

    def _get_existing_relation(self, target_organization: Organization) -> Optional[OrganizationRelation]:
        """Get existing relation if it exists."""
        try:
            return OrganizationRelation.objects.get(
                organization_from=self.organization,
                organization_to=target_organization
            )
        except OrganizationRelation.DoesNotExist:
            return None

    def _create_initial_relation(self, target_organization: Organization) -> BehaviorModel:
        """Create initial relation based on target organization's default behavior."""
        relation_type = (
            BehaviorModel.AGGRESSIVE
            if target_organization.behavior == BehaviorModel.AGGRESSIVE
            else BehaviorModel.PASSIVE
        )

        OrganizationRelation.objects.create(
            organization_from=self.organization,
            organization_to=target_organization,
            type=relation_type
        )

        return relation_type

    @transaction.atomic
    def recalculate_relation_with(self, target_organization: Organization) -> BehaviorModel:
        """
        Recalculate organization relationship based on all character relationships.

        This method should be called when character relationships change.

        Args:
            target_organization: The organization to recalculate relationship with

        Returns:
            The new relationship type
        """
        relation = self._get_existing_relation(target_organization)

        # Don't change immutable relations
        if relation and relation.immutable:
            return relation.type

        # Get character relationship counts efficiently
        relation_counts = self._get_character_relation_counts(target_organization)

        # Determine new relation type
        new_type = RelationshipCalculator.determine_relation_from_counts(
            relation_counts[BehaviorModel.AGGRESSIVE],
            relation_counts[BehaviorModel.FRIENDLY],
            relation_counts[BehaviorModel.PASSIVE]
        )

        # Update or create the relation
        if relation:
            relation.type = new_type
            relation.save(update_fields=['type'])
        else:
            OrganizationRelation.objects.create(
                organization_from=self.organization,
                organization_to=target_organization,
                type=new_type
            )

        return new_type

    def _get_character_relation_counts(self, target_organization: Organization) -> Dict[BehaviorModel, int]:
        """
        Efficiently count character relationships between organizations.

        Args:
            target_organization: The target organization

        Returns:
            Dictionary with counts for each relationship type
        """
        # Get all characters from both organizations
        our_character_ids = list(
            Character.objects.filter(organization=self.organization)
            .values_list('id', flat=True)
        )
        their_character_ids = list(
            Character.objects.filter(organization=target_organization)
            .values_list('id', flat=True)
        )

        if not our_character_ids or not their_character_ids:
            return {BehaviorModel.AGGRESSIVE: 0, BehaviorModel.FRIENDLY: 0, BehaviorModel.PASSIVE: 0}

        # Count existing relations efficiently
        relation_counts = CharacterRelation.objects.filter(
            character_from_id__in=our_character_ids,
            character_to_id__in=their_character_ids
        ).values('type').annotate(count=Count('type'))

        # Convert to dictionary
        counts = {BehaviorModel.AGGRESSIVE: 0, BehaviorModel.FRIENDLY: 0, BehaviorModel.PASSIVE: 0}
        for item in relation_counts:
            if item['type'] == BehaviorModel.AGGRESSIVE:
                counts[BehaviorModel.AGGRESSIVE] = item['count']
            elif item['type'] == BehaviorModel.FRIENDLY:
                counts[BehaviorModel.FRIENDLY] = item['count']
            else:
                counts[BehaviorModel.PASSIVE] = item['count']

        # Add count for characters without explicit relations (treated as passive)
        total_possible_relations = len(our_character_ids) * len(their_character_ids)
        explicit_relations = sum(counts.values())
        counts[BehaviorModel.PASSIVE] += total_possible_relations - explicit_relations

        return counts


class CharacterRelationService:
    """
    Service for managing relationships between characters.

    This service handles:
    1. Acquiring character relationships based on organization relations and default behaviors
    2. Updating character relationships and triggering organization recalculation
    3. Ensuring relationship consistency and immutability rules
    """

    def __init__(self, character: CharacterService):
        self.character = character
        self._org_service = None

    @property
    def organization_service(self) -> Optional[OrganizationRelationService]:
        """Lazy-loaded organization service to avoid circular dependencies."""
        if self._org_service is None and self.character.model.organization:
            self._org_service = OrganizationRelationService(self.character.model.organization)
        return self._org_service

    def get_relation_to(self, target_character: CharacterService) -> BehaviorModel:
        """
        Get the relationship type to another character.
        Creates the relationship if it doesn't exist based on organization relations and default behaviors.

        Args:
            target_character: The character to get a relationship with

        Returns:
            The relationship type (BehaviorModel)
        """
        if self.character.model.id == target_character.model.id:
            return BehaviorModel.FRIENDLY

        if self.character.model.organization == target_character.model.organization:
            return BehaviorModel.FRIENDLY

        relation = self._get_existing_relation(target_character)

        if relation:
            return relation.type

        return self._create_initial_relation(target_character)

    def _get_existing_relation(self, target_character: CharacterService) -> Optional[CharacterRelation]:
        """Get an existing relation if it exists."""
        try:
            return CharacterRelation.objects.get(
                character_from=self.character.model,
                character_to=target_character.model
            )
        except CharacterRelation.DoesNotExist:
            return None

    def _create_initial_relation(self, target_character: CharacterService) -> BehaviorModel:
        """Create initial relation based on organization relations and default behaviors."""
        relation_type = self.character.model.behavior  # Default

        if relation_type != BehaviorModel.AGGRESSIVE:
            # Check organization relationship first
            if (self.organization_service and
                    target_character.model.organization and
                    self.character.model.organization != target_character.model.organization):

                org_relation = self.organization_service.get_relation_to(target_character.model.organization)
                if org_relation == BehaviorModel.AGGRESSIVE:
                    relation_type = BehaviorModel.AGGRESSIVE

            # Override with character's default behavior if aggressive
            if target_character.model.behavior == BehaviorModel.AGGRESSIVE:
                relation_type = BehaviorModel.AGGRESSIVE

        CharacterRelation.objects.create(
            character_from=self.character.model,
            character_to=target_character.model,
            type=relation_type
        )

        return relation_type

    @transaction.atomic
    def set_relation_to(self, target_character: CharacterService, relation_type: BehaviorModel) -> bool:
        """
        Set the relationship type to another character.

        Args:
            target_character: The character to set relationship with
            relation_type: The desired relationship type

        Returns:
            True if the relationship was changed, False if it was immutable
        """
        relation = self._get_existing_relation(target_character)

        if relation:
            if relation.immutable:
                return False
            if relation.type == relation_type:
                return True # No change needed
            relation.type = relation_type
            relation.save(update_fields=['type'])
        else:
            CharacterRelation.objects.create(
                character_from=self.character.model,
                character_to=target_character.model,
                type=relation_type
            )

        # Trigger organization relationship recalculation
        self._trigger_organization_recalculation(target_character)
        return True

    def become_aggressive_to(self, target_character: CharacterService) -> bool:
        """Make this character aggressive towards the target character."""
        return self.set_relation_to(target_character, BehaviorModel.AGGRESSIVE)

    def become_friendly_to(self, target_character: CharacterService) -> bool:
        """Make this character friendly towards the target character."""
        return self.set_relation_to(target_character, BehaviorModel.FRIENDLY)

    def become_passive_to(self, target_character: CharacterService) -> bool:
        """Make this character passive towards the target character."""
        return self.set_relation_to(target_character, BehaviorModel.PASSIVE)

    def _trigger_organization_recalculation(self, target_character: CharacterService) -> None:
        """Trigger organization relationship recalculation if applicable."""
        if (self.organization_service and
                target_character.model.organization and
                self.character.model.organization != target_character.model.organization):
            self.organization_service.recalculate_relation_with(target_character.model.organization)


# Convenience functions for external usage
def get_organization_relation_service(organization: Organization) -> OrganizationRelationService:
    """Factory function to create OrganizationRelationService."""
    return OrganizationRelationService(organization)


def get_character_relation_service(character: CharacterService) -> CharacterRelationService:
    """Factory function to create CharacterRelationService."""
    return CharacterRelationService(character)
