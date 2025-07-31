import logging
import typing as t

from django.db.models import Q

from apps.fight.models import Fight
from apps.character.models import Character
from apps.game.services.character.core import CharacterService

if t.TYPE_CHECKING:
    from apps.game.services.notifier.base import BaseNotifier


class FightAutoJoiner:
    """
    Detects the active fights and their positions, finds if there are any characters in the same position 
    and not in the fight and adds them to the fight.
    
    1. Finds all active fights in the current Cycle.
    2. For each fight, finds all characters in the same position that are not in the fight.
    3. For each character found, adds them to the fight as pending joiners.
    4. Emits the CharacterPendingJoinFight event to all characters in that position.
    5. Emits the PendingJoinFight event to the character who joined the fight.
    """

    def __init__(self, notifier: "BaseNotifier"):
        self.notifier = notifier
        self.logger = logging.getLogger("game.services.fight.FightAutoJoiner")

    def process_auto_joins(self, campaign) -> dict[int, list]:
        """
        Process automatic fight joins for all active fights in the campaign.
        
        Args:
            campaign: Campaign instance to process fights for
            
        Returns:
            Dict mapping fight IDs to lists of characters that were added as pending joiners
        """
        active_fights = self._get_active_fights(campaign)
        results = {}

        for fight in active_fights:
            pending_joiners = self._process_fight_auto_join(fight)
            if pending_joiners:
                results[fight.id] = pending_joiners

        self.logger.info(f"Processed auto-joins for {len(active_fights)} fights, "
                         f"added {sum(len(joiners) for joiners in results.values())} pending joiners")
        return results

    def _get_active_fights(self, campaign) -> list[Fight]:
        """Get all active (open) fights in the campaign."""
        return list(Fight.objects.filter(
            open=True,
            ended_at__isnull=True,
            campaign=campaign
        ).select_related('position', 'attacker', 'defender').prefetch_related('pending_join'))

    def _process_fight_auto_join(self, fight: Fight) -> list[Character]:
        """
        Process auto-join for a single fight.
        
        Args:
            fight: Fight instance to process
            
        Returns:
            List of characters added as pending joiners
        """
        potential_joiners = self._find_potential_joiners(fight)
        added_joiners = []

        for character in potential_joiners:
            if self._should_add_to_pending(fight, character):
                self._add_to_pending_join(fight, character)
                added_joiners.append(character)
                self._emit_pending_join_events(fight, character)

        return added_joiners

    def _find_potential_joiners(self, fight: Fight) -> list[Character]:
        """
        Find characters at the same position who could potentially join the fight.
        
        Args:
            fight: Fight instance
            
        Returns:
            List of potential joiner characters
        """
        return list(Character.objects.filter(
            position=fight.position,
            is_active=True,
            fight__isnull=True  # Not already in any fight
        ).exclude(
            Q(id=fight.attacker.id) | Q(id=fight.defender.id)
        ).exclude(
            id__in=fight.pending_join.values_list('id', flat=True)
        ))

    def _should_add_to_pending(self, fight: Fight, character: Character) -> bool:
        """
        Determine if a character should be added to pending joiners.
        
        Args:
            fight: Fight instance
            character: Character to evaluate
            
        Returns:
            bool: True if character should be added to pending joiners
        """
        # Check if character is already in a fight using the fight field
        if character.fight and character.fight != fight:
            self.logger.debug(f"Character {character} is already in fight {character.fight.id}")
            return False

        # Check if character has enough health to participate
        if hasattr(character, 'current_health') and character.current_health <= 0:
            self.logger.debug(f"Character {character} has no health to join fight")
            return False

        # Check if character is in a state that prevents fighting (e.g., unconscious, etc.)
        if self._is_character_incapacitated(character):
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
        # Check for incapacitating effects
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

        return active_effects.exists()

    def _add_to_pending_join(self, fight: Fight, character: Character):
        """
        Add character to fight's pending joiners.
        
        Args:
            fight: Fight instance
            character: Character to add
        """
        try:
            fight.pending_join.add(character)
            self.logger.debug(f"Added {character} to pending joiners for fight {fight.id}")
            svc = CharacterService(character)
            svc.spend_all_ap()
            self.logger.debug(f"Spent all AP for character {character.id} in fight {fight.id}")
        except Exception as e:
            self.logger.error(f"Failed to add {character} to pending joiners for fight {fight.id}: {e}")

    def _emit_pending_join_events(self, fight: Fight, character: Character):
        """
        Emit events for a character being added to pending joiners.
        
        Args:
            fight: Fight instance
            character: Character that was added to pending joiners
        """
        try:
            # Emit event to all characters at the position
            self._emit_character_pending_join_fight_event(fight, character)

            # Emit event to the specific character
            self._emit_pending_join_fight_event(fight, character)

        except Exception as e:
            self.logger.error(f"Failed to emit pending join events for {character} in fight {fight.id}: {e}")

    def _emit_character_pending_join_fight_event(self, fight: Fight, character: Character):
        """
        Emit CharacterPendingJoinFight event to all characters at the position.
        
        Args:
            fight: Fight instance
            character: Character joining as pending
        """
        try:
            from apps.core.bus.events.fight.produced import CharacterPendingJoinFightEvent

            event = CharacterPendingJoinFightEvent.create_event(
                fight_id=fight.id,
                character_id=character.id,
                position_id=fight.position.id
            )

            self.notifier.bus.publish(event)
            self.logger.debug(f"Emitted CharacterPendingJoinFight event for {character} in fight {fight.id}")

        except ImportError:
            self.logger.warning("CharacterPendingJoinFightEvent not implemented yet")
        except Exception as e:
            self.logger.error(f"Failed to emit CharacterPendingJoinFight event: {e}")

    def _emit_pending_join_fight_event(self, fight: Fight, character: Character):
        """
        Emit PendingJoinFight event to the specific character.
        
        Args:
            fight: Fight instance
            character: Character joining as pending
        """
        try:
            from apps.core.bus.events.fight.produced import PendingJoinFightEvent

            event = PendingJoinFightEvent.create_event(
                fight_id=fight.id,
                character_id=character.id
            )

            self.notifier.bus.publish(event)
            self.logger.debug(f"Emitted PendingJoinFight event for {character} in fight {fight.id}")

        except ImportError:
            self.logger.warning("PendingJoinFightEvent not implemented yet")
        except Exception as e:
            self.logger.error(f"Failed to emit PendingJoinFight event: {e}")
