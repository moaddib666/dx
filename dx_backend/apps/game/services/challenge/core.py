import logging
from typing import List, Dict, Any, Optional

from django.db import transaction

from apps.character.models import Character
from apps.core.bus.events.challenge.produced.challenge_events import ChallengeCreatedEvent
from apps.core.bus.pubsub import event_bus
from apps.core.models import CharacterStats
from apps.core.models.dice import ChallengeCreationRequest
from apps.dice.models import Challenge, ChallengeModifier
from apps.game.services.character.core import CharacterService


class ChallengeService:
    """Service for managing challenge creation and assignment."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    @transaction.atomic
    def create_challenge_for_character(
        self,
        target_character: Character,
        request: ChallengeCreationRequest
    ) -> Challenge:
        """
        Create a new challenge for a character with business logic using DTO.
        
        Args:
            target_character: The character who will face the challenge
            request: ChallengeCreationRequest DTO containing all challenge parameters
        
        Returns:
            The created Challenge instance
        """
        self.logger.info(f"Creating challenge for character {target_character.name}")
        
        # Create the challenge
        challenge = Challenge.objects.create(
            target=target_character,
            difficulty=request.difficulty,
            dice_sides=request.dice_sides,
            stat=request.stat,
            advantage=request.advantage,
            disadvantage=request.disadvantage,
            description=request.description or ""
        )
        
        # Add modifiers if provided
        if request.modifiers:
            self._add_modifiers_from_dto(challenge, request.modifiers)
        
        # Add automatic modifiers based on character state
        self._add_automatic_modifiers(challenge, target_character)
        
        # Set the challenge as the character's current challenge
        target_character.challenge = challenge
        target_character.save(update_fields=['challenge'])
        
        # Fire event via event bus
        self._notify_challenge_created(challenge)
        
        self.logger.info(f"Challenge {challenge.id} created successfully for {target_character.name}")
        return challenge
    
    def _add_modifiers_from_dto(self, challenge: Challenge, modifiers):
        """Add explicit modifiers to the challenge from DTO."""
        from apps.core.models.dice import ChallengeModifierRequest
        
        for modifier_request in modifiers:
            ChallengeModifier.objects.create(
                challenge=challenge,
                name=modifier_request.name,
                value=modifier_request.value,
                icon=modifier_request.icon
            )
    
    def _add_automatic_modifiers(self, challenge: Challenge, character: Character):
        """
        Add automatic modifiers based on character state, stats, effects, skills, and items.
        This is where business logic for automatic modifiers would be implemented.
        """
        character_service = CharacterService(character)
        
        # Example: Add modifier based on character's current health
        current_hp_percentage = character_service.get_current_hp() / character_service.get_max_hp()
        if current_hp_percentage < 0.25:  # Less than 25% health
            ChallengeModifier.objects.create(
                challenge=challenge,
                name="Severely Wounded",
                value=-2  # Penalty for being severely wounded
            )
        elif current_hp_percentage < 0.5:  # Less than 50% health
            ChallengeModifier.objects.create(
                challenge=challenge,
                name="Wounded",
                value=-1  # Minor penalty for being wounded
            )
        
        # Example: Add modifier based on character's energy
        current_energy_percentage = character_service.get_current_energy() / character_service.get_max_energy()
        if current_energy_percentage < 0.25:  # Less than 25% energy
            ChallengeModifier.objects.create(
                challenge=challenge,
                name="Exhausted",
                value=-1  # Penalty for being exhausted
            )
        
        # TODO: Add more automatic modifiers based on:
        # - Active effects on the character
        # - Character's skills relevant to the challenge
        # - Equipped items that might help or hinder
        # - Environmental factors
        # - Character's rank and experience
        
        self.logger.debug(f"Added automatic modifiers to challenge {challenge.id}")
    
    def _notify_challenge_created(self, challenge: Challenge):
        """Send event notification that a challenge was created using properly typed events."""
        # Count modifiers for the event
        modifier_count = challenge.modifiers.count()
        
        # Create properly typed event using the create_event class method
        event = ChallengeCreatedEvent.create_event(
            challenge_id=challenge.id,
            target_character_id=challenge.target.id,
            difficulty=challenge.difficulty,
            dice_sides=challenge.dice_sides,
            stat=challenge.stat,
            advantage=challenge.advantage,
            disadvantage=challenge.disadvantage,
            description=challenge.description,
            modifier_count=modifier_count
        )
        
        event_bus.publish(event)
        self.logger.debug(f"Published challenge_created event for challenge {challenge.id}")