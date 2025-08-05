import logging
import typing as t

from django.db.models import Q

from apps.core.models import ImpactType
from apps.fight.models import Fight
from apps.character.models import Character
from apps.game.services.character.core import CharacterService
from apps.action.models import Cycle

if t.TYPE_CHECKING:
    from apps.game.services.notifier.base import BaseNotifier


class FightCloser:
    """
    Detects when fights have ended by inspecting last cycle actions, closes the fight, 
    emits events and removes all characters from the fight.

    1. Find all active fight participants in the current Cycle.
    2. Exclude characters that do not have health. 
    3. If nobody left in the fight, close the fight.
    4. Check previous Cycle actions if no actions were made in the previous Cycle, close the fight.
    5. Emit the FightEnded event to all characters in the position.
    6. Remove all characters from the fight.
    """

    def __init__(self, notifier: "BaseNotifier"):
        self.notifier = notifier
        self.logger = logging.getLogger("game.services.fight.FightCloser")

    def process_fight_endings(self, cycle: "Cycle") -> list[Fight]:
        """
        Process fight endings for all active fights in the campaign.
        
        Returns:
            List of fights that were closed
        """
        active_fights = self._get_active_fights(cycle)
        closed_fights = []

        for fight in active_fights:
            if self._should_close_fight(fight, cycle):
                if self._close_fight(fight, cycle):
                    closed_fights.append(fight)
                    self._emit_fight_ended_events(fight)

        self.logger.info(f"Processed {len(active_fights)} active fights, closed {len(closed_fights)}")
        return closed_fights

    def _get_active_fights(self, cycle: "Cycle") -> list[Fight]:
        """Get all active fights in the current campaign."""
        return list(Fight.objects.filter(
            open=True,
            campaign=cycle.campaign
        ).select_related('position', 'attacker', 'defender').prefetch_related('pending_joiners'))

    def _should_close_fight(self, fight: Fight, cycle: "Cycle") -> bool:
        """
        Determine if a fight should be closed.
        
        Args:
            fight: Fight instance to evaluate
            
        Returns:
            bool: True if fight should be closed
        """
        # Check if no viable participants remain
        if not self._has_viable_participants(fight):
            self.logger.debug(f"Fight {fight.id} has no viable participants")
            return True

        # Check for inactivity
        if self._is_fight_inactive(fight, cycle):
            self.logger.debug(f"Fight {fight.id} is inactive")
            return True

        # Check if all participants have left the position
        if not self._has_participants_at_position(fight):
            self.logger.debug(f"Fight {fight.id} has no participants at position")
            return True

        return False

    def _has_viable_participants(self, fight: Fight) -> bool:
        """
        Check if the fight has viable participants (characters who can continue fighting).
        
        Args:
            fight: Fight instance to check
            
        Returns:
            bool: True if a fight has viable participants
        """
        viable_count = 0

        # Check main participants
        main_participants = fight.joined.filter(
            current_health_points__gt=0,
            is_active=True
        )
        pending_joiners = fight.pending_joiners.filter(
            character__current_health_points__gt=0,
            character__is_active=True
        )
        # TODO: check if the any npc character in fight ....
        # TODO: prefetch related active effects to optimize this query
        for character in main_participants:
            if character and self._is_character_viable(character):
                self.logger.debug(f"Character {character.id} is viable for fight {fight.id}")
                viable_count += 1

        # Check pending joiners
        for pending_record in pending_joiners:
            if self._is_character_viable(pending_record.character):
                self.logger.debug(f"Pending joiner {pending_record.character.id} is viable for fight {fight.id}")
                viable_count += 1

        # Need at least 2 viable participants for a fight
        return viable_count >= 2

    def _is_character_viable(self, character: Character) -> bool:
        """
        Check if a character is viable for continuing the fight.
        
        Args:
            character: Character to check
            
        Returns:
            bool: True if character is viable
        """
        svc = CharacterService(character)

        # Check if character is knocked out
        if svc.is_knocked_out():
            self.logger.debug(f"Character {character.id} is knocked out and cannot continue fighting")
            return False

        # Check if the character is active
        if not character.is_active:
            return False

        # Check for incapacitating effects
        if self._is_character_incapacitated(character):
            return False

        return True

    def _is_character_incapacitated(self, character: Character) -> bool:
        """
        Check if character is incapacitated and cannot continue fighting.

        Args:
            character: Character to check

        Returns:
            bool: True if character is incapacitated
        """
        from apps.core.models import EffectType

        fight_ending_effects = {
            EffectType.KNOCKED_OUT,
            EffectType.COMA,
        }

        active_effects = character.effects.filter(
            effect__id__in=fight_ending_effects
        )

        return active_effects.exists()

    def _is_fight_inactive(self, fight: Fight, cycle: "Cycle") -> bool:
        """
        Check if the fight is inactive (no actions from participants in recent cycles).
        
        Args:
            fight: Fight instance to check
            
        Returns:
            bool: True if a fight is inactive
        """
        if cycle.number == 0:
            return False
        n_cycles = 2
        fight_cycles = Cycle.objects.filter(
            campaign=fight.campaign,
            number__lt=cycle.number,
            number__gte=fight.created.number
        ).order_by('-number')
        if fight_cycles.count() <= n_cycles:
            return False
        last_n_cycles = fight_cycles[:n_cycles]

        offensive_actions = fight.actions.filter(
            cycle__in=last_n_cycles,
            impacts__type__in=ImpactType.get_aggressive_types(),
            performed=True,
        )

        # If no actions from participants in recent cycles, the fight is inactive
        return not offensive_actions.exists()

    def _has_participants_at_position(self, fight: Fight) -> bool:
        """
        Check if the fight has participants still at the fight position.
        
        Args:
            fight: Fight instance to check
            
        Returns:
            bool: True if participants are still at the position
        """
        # Check main participants
        main_participants = [fight.attacker, fight.defender]
        for character in main_participants:
            if character and character.position == fight.position and character.is_active:
                return True

        # Check pending joiners
        for character in fight.pending_join.all():
            if character.position == fight.position and character.is_active:
                return True

        return False

    def _close_fight(self, fight: Fight, cycle: "Cycle") -> bool:
        """
        Close a fight and clean up its state.
        
        Args:
            fight: Fight instance to close
            
        Returns:
            bool: True if fight was successfully closed
        """
        try:
            # Set the fight as closed
            fight.open = False
            fight.ended_at = cycle
            fight.save()

            # Clear Character.fight field for all participants
            self._clear_character_fight_fields(fight)

            # Clear pending joiners
            fight.pending_joiners.all().delete()

            self.logger.info(f"Closed fight {fight.id} in cycle {cycle.number}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to close fight {fight.id}: {e}")
            return False

    def _clear_character_fight_fields(self, fight: Fight):
        """
        Clear Character.fight field for all participants in the fight.
        
        Args:
            fight: Fight instance being closed
        """
        try:
            Character.objects.filter(
                fight=fight
            ).update(fight=None)
            self.logger.debug(f"Cleared fight field for all characters in fight {fight.id}")
        except Exception as e:
            self.logger.error(f"Failed to clear character fight fields for fight {fight.id}: {e}")

    def _emit_fight_ended_events(self, fight: Fight):
        """
        Emit FightEnded events to all characters at the position.
        
        Args:
            fight: Fight instance that ended
        """
        try:
            self._emit_fight_ended_event(fight)

        except Exception as e:
            self.logger.error(f"Failed to emit fight ended events for fight {fight.id}: {e}")

    def _emit_fight_ended_event(self, fight: Fight):
        """
        Emit FightEnded event to all characters at the position.
        
        Args:
            fight: Fight instance that ended
        """
        try:
            from apps.core.bus.events.fight.produced import FightEndedEvent

            event = FightEndedEvent.create_event(
                fight_id=fight.id,
                position_id=fight.position.id,
                cycle_id=cycle.id
            )

            self.notifier.bus.publish(event)
            self.logger.debug(f"Emitted FightEnded event for fight {fight.id}")

        except ImportError:
            self.logger.warning("FightEndedEvent not implemented yet")
        except Exception as e:
            self.logger.error(f"Failed to emit FightEnded event: {e}")

    def force_close_fight(self, fight: Fight, cycle: "Cycle", reason: str = "Manually closed") -> bool:
        """
        Force close a fight regardless of normal conditions.
        
        Args:
            fight: Fight instance to close
            reason: Reason for forcing closure
            
        Returns:
            bool: True if successful
        """
        try:
            self.logger.info(f"Force closing fight {fight.id}: {reason}")

            if self._close_fight(fight, cycle):
                self._emit_fight_ended_events(fight)
                return True
            return False

        except Exception as e:
            self.logger.error(f"Failed to force close fight {fight.id}: {e}")
            return False
