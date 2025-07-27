import logging
import typing as t

from apps.fight.models import Fight
from apps.character.models import Character

if t.TYPE_CHECKING:
    from apps.game.services.notifier.base import BaseNotifier


class FightPendingJoiner:
    """
    Handles the pending joiners in the fight.
    
    1. Find all characters in the fight that are pending to join.
    2. Check that a fight is still open and could be joined.
    3. Remove characters from the pending joiners list.
    4. Emit the CharacterJoinFight event to characters in the location of the fight.
    5. Emit the JoinedFight event to the character who joined the fight.
    """

    def __init__(self, notifier: "BaseNotifier"):
        self.notifier = notifier
        self.logger = logging.getLogger("game.services.fight.FightPendingJoiner")

    def process_pending_joiners(self, campaign) -> dict[int, list]:
        """
        Process pending joiners for all fights in the campaign.
        
        Args:
            campaign: Campaign instance to process fights for
            
        Returns:
            Dict mapping fight IDs to lists of characters that joined
        """
        active_fights = self._get_active_fights_with_pending(campaign)
        results = {}

        for fight in active_fights:
            joined_characters = self._process_fight_pending_joiners(fight)
            if joined_characters:
                results[fight.id] = joined_characters

        self.logger.info(f"Processed pending joiners for {len(active_fights)} fights, "
                         f"converted {sum(len(joiners) for joiners in results.values())} to active participants")
        return results

    def _get_active_fights_with_pending(self, campaign) -> list[Fight]:
        """Get active fights that have pending joiners."""
        return list(Fight.objects.filter(
            open=True,
            position__campaign=campaign,
            pending_join__isnull=False
        ).distinct().select_related('position').prefetch_related('pending_join'))

    def _process_fight_pending_joiners(self, fight: Fight) -> list[Character]:
        """
        Process pending joiners for a single fight.
        
        Args:
            fight: Fight instance to process
            
        Returns:
            List of characters that successfully joined the fight
        """
        pending_characters = list(fight.pending_join.all())
        joined_characters = []

        for character in pending_characters:
            if self._should_join_fight(fight, character):
                if self._convert_to_active_participant(fight, character):
                    joined_characters.append(character)
                    self._emit_join_events(fight, character)

        return joined_characters

    def _should_join_fight(self, fight: Fight, character: Character) -> bool:
        """
        Determine if a pending character should join the fight.
        
        Args:
            fight: Fight instance
            character: Character to evaluate
            
        Returns:
            bool: True if character should join the fight
        """
        # Check if fight is still open
        if not fight.open:
            self.logger.debug(f"Fight {fight.id} is closed, cannot join")
            return False

        # Check if character is still active
        if not character.is_active:
            self.logger.debug(f"Character {character} is not active")
            return False

        # Check if character is still at the fight position
        if character.position != fight.position:
            self.logger.debug(f"Character {character} is no longer at fight position")
            return False

        # Check if character is capable of fighting
        if self._is_character_incapacitated(character):
            return False

        # Check if fight has room for more participants
        if not self._fight_has_capacity(fight):
            return False

        return True

    def _is_character_incapacitated(self, character: Character) -> bool:
        """
        Check if character is incapacitated and cannot join fights.
        
        Args:
            character: Character to check
            
        Returns:
            bool: True if character is incapacitated
        """
        from apps.core.models import EffectType

        incapacitating_effects = {
            EffectType.KNOCKED_OUT,
            EffectType.COMA,
            EffectType.SLEEPING,
            EffectType.PARALYZED
        }

        active_effects = character.effects.filter(
            effect__id__in=incapacitating_effects
        )

        if active_effects.exists():
            self.logger.debug(f"Character {character} is incapacitated")
            return True

        # Check health status
        if hasattr(character, 'current_health') and character.current_health <= 0:
            self.logger.debug(f"Character {character} has no health")
            return True

        return False

    def _fight_has_capacity(self, fight: Fight) -> bool:
        """
        Check if the fight has capacity for more participants.
        
        Args:
            fight: Fight instance to check
            
        Returns:
            bool: True if fight can accept more participants
        """
        # For now, we'll allow unlimited participants in fights
        # This could be configured based on fight type or position constraints
        max_participants = getattr(fight, 'max_participants', None)

        if max_participants is None:
            return True

        current_participants = 2  # attacker + defender
        current_participants += fight.pending_join.count()

        return current_participants < max_participants

    def _convert_to_active_participant(self, fight: Fight, character: Character) -> bool:
        """
        Convert a pending joiner to an active participant in the fight.
        
        Args:
            fight: Fight instance
            character: Character to convert
            
        Returns:
            bool: True if conversion was successful
        """
        try:
            # Remove from pending joiners
            fight.pending_join.remove(character)

            # Set Character.fight field to mark them as active participant
            character.fight = fight
            character.save(update_fields=['fight'])

            self.logger.info(f"Converted {character} from pending to active participant in fight {fight.id}")
            self.logger.debug(f"Set fight field for character {character.id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to convert {character} to active participant in fight {fight.id}: {e}")
            return False

    def _emit_join_events(self, fight: Fight, character: Character):
        """
        Emit events for a character joining the fight.
        
        Args:
            fight: Fight instance
            character: Character that joined
        """
        try:
            # Emit event to all characters at the position
            self._emit_character_join_fight_event(fight, character)

            # Emit event to the specific character
            self._emit_joined_fight_event(fight, character)

        except Exception as e:
            self.logger.error(f"Failed to emit join events for {character} joining fight {fight.id}: {e}")

    def _emit_character_join_fight_event(self, fight: Fight, character: Character):
        """
        Emit CharacterJoinFight event to all characters at the position.
        
        Args:
            fight: Fight instance
            character: Character joining
        """
        try:
            from apps.core.bus.events.fight.produced import CharacterJoinFightEvent

            event = CharacterJoinFightEvent.create_event(
                fight_id=fight.id,
                character_id=character.id,
                position_id=fight.position.id
            )

            self.notifier.bus.publish(event)
            self.logger.debug(f"Emitted CharacterJoinFight event for {character} joining fight {fight.id}")

        except ImportError:
            self.logger.warning("CharacterJoinFightEvent not implemented yet")
        except Exception as e:
            self.logger.error(f"Failed to emit CharacterJoinFight event: {e}")

    def _emit_joined_fight_event(self, fight: Fight, character: Character):
        """
        Emit JoinedFight event to the specific character.
        
        Args:
            fight: Fight instance
            character: Character joining
        """
        try:
            from apps.core.bus.events.fight.produced import JoinedFightEvent

            event = JoinedFightEvent.create_event(
                fight_id=fight.id,
                character_id=character.id
            )

            self.notifier.bus.publish(event)
            self.logger.debug(f"Emitted JoinedFight event for {character} joining fight {fight.id}")

        except ImportError:
            self.logger.warning("JoinedFightEvent not implemented yet")
        except Exception as e:
            self.logger.error(f"Failed to emit JoinedFight event: {e}")

    def force_join_character(self, fight: Fight, character: Character) -> bool:
        """
        Force a character to join a fight (bypassing normal checks).
        
        Args:
            fight: Fight instance
            character: Character to force join
            
        Returns:
            bool: True if successful
        """
        try:
            if character in fight.pending_join.all():
                return self._convert_to_active_participant(fight, character)
            else:
                # Character wasn't pending, so just emit events
                self._emit_join_events(fight, character)
                return True

        except Exception as e:
            self.logger.error(f"Failed to force join {character} to fight {fight.id}: {e}")
            return False
