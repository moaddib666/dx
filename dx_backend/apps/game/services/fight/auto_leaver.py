import logging
import typing as t

from django.db.models import Q

from apps.fight.models import Fight
from apps.character.models import Character

if t.TYPE_CHECKING:
    from apps.game.services.notifier.base import BaseNotifier


class FightAutoLeaver:
    """
    Detaches characters from fights that are not active anymore, or if characters change their position 
    from the fight position.
    
    1. Find all characters in the fight.
    2. For each character, check if the fight is still active or if the character has changed their position.
    3. If the fight is not active or the character has changed their position, remove the character from the fight.
    4. Emit the CharacterLeaveFight event to characters at the position.
    5. Emit the LeftFight event to the character who left the fight.
    """

    def __init__(self, notifier: "BaseNotifier"):
        self.notifier = notifier
        self.logger = logging.getLogger("game.services.fight.FightAuthLeaver")

    def process_authorized_leavers(self, campaign) -> dict[int, list]:
        """
        Process authorized leaving for all fights in the campaign.
        
        Args:
            campaign: Campaign instance to process fights for
            
        Returns:
            Dict mapping fight IDs to lists of characters that left
        """
        all_fights = self._get_all_fights(campaign)
        results = {}

        for fight in all_fights:
            leavers = self._process_fight_leavers(fight)
            if leavers:
                results[fight.id] = leavers

        self.logger.info(f"Processed leavers for {len(all_fights)} fights, "
                         f"removed {sum(len(leavers) for leavers in results.values())} characters")
        return results

    def _get_all_fights(self, campaign) -> list[Fight]:
        """Get all fights in the campaign (both active and inactive)."""
        return list(Fight.objects.filter(
            position__campaign=campaign
        ).select_related('position', 'attacker', 'defender').prefetch_related('pending_join'))

    def _process_fight_leavers(self, fight: Fight) -> list[Character]:
        """
        Process leaving for a single fight.
        
        Args:
            fight: Fight instance to process
            
        Returns:
            List of characters that left the fight
        """
        leavers = []

        # Check main participants (attacker and defender)
        main_participants = [fight.attacker, fight.defender]
        for character in main_participants:
            if character and self._should_character_leave(fight, character):
                if self._remove_main_participant(fight, character):
                    # Clear Character.fight field
                    character.fight = None
                    character.save(update_fields=['fight'])
                    leavers.append(character)
                    self._emit_leave_events(fight, character)

        # Check pending joiners
        pending_joiners = list(fight.pending_join.all())
        for character in pending_joiners:
            if self._should_character_leave(fight, character):
                self._remove_pending_joiner(fight, character)
                # Clear Character.fight field if it matches this fight
                if character.fight == fight:
                    character.fight = None
                    character.save(update_fields=['fight'])
                leavers.append(character)
                self._emit_leave_events(fight, character)

        return leavers

    def _should_character_leave(self, fight: Fight, character: Character) -> bool:
        """
        Determine if a character should leave the fight.
        
        Args:
            fight: Fight instance
            character: Character to evaluate
            
        Returns:
            bool: True if character should leave the fight
        """
        # Check if fight is no longer active and character should be removed
        if not fight.open and not self._is_fight_ending_gracefully(fight):
            self.logger.debug(f"Fight {fight.id} is closed, removing {character}")
            return True

        # Check if character changed position
        if character.position != fight.position:
            self.logger.debug(f"Character {character} changed position from {fight.position} to {character.position}")
            return True

        # Check if character is no longer active
        if not character.is_active:
            self.logger.debug(f"Character {character} is no longer active")
            return True

        # Check if character is incapacitated beyond recovery in this fight
        if self._is_character_permanently_incapacitated(character):
            return True

        return False

    def _is_fight_ending_gracefully(self, fight: Fight) -> bool:
        """
        Check if the fight is ending gracefully (e.g., through proper game mechanics).
        
        Args:
            fight: Fight instance to check
            
        Returns:
            bool: True if fight is ending gracefully
        """
        # If fight has an end cycle, it's ending gracefully
        return fight.ended_at is not None

    def _is_character_permanently_incapacitated(self, character: Character) -> bool:
        """
        Check if character is permanently incapacitated for this fight.
        
        Args:
            character: Character to check
            
        Returns:
            bool: True if character is permanently incapacitated
        """
        from apps.core.models import EffectType

        # Characters in coma should be removed from fights
        permanently_incapacitating_effects = {
            EffectType.COMA,
        }

        active_effects = character.effects.filter(
            effect__id__in=permanently_incapacitating_effects
        )

        return active_effects.exists()

    def _remove_main_participant(self, fight: Fight, character: Character) -> bool:
        """
        Remove a main participant (attacker or defender) from the fight.
        
        Args:
            fight: Fight instance
            character: Character to remove
            
        Returns:
            bool: True if character was successfully removed
        """
        try:
            if character == fight.attacker:
                # If attacker leaves, try to promote defender or close fight
                return self._handle_attacker_leaving(fight)
            elif character == fight.defender:
                # If defender leaves, try to promote pending joiner or close fight
                return self._handle_defender_leaving(fight)
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove main participant {character} from fight {fight.id}: {e}")
            return False

    def _handle_attacker_leaving(self, fight: Fight) -> bool:
        """
        Handle the attacker leaving the fight.
        
        Args:
            fight: Fight instance
            
        Returns:
            bool: True if attacker was successfully handled
        """
        # Try to promote a pending joiner to attacker
        pending_joiners = fight.pending_join.filter(is_active=True)
        if pending_joiners.exists():
            new_attacker = pending_joiners.first()
            fight.pending_join.remove(new_attacker)
            fight.attacker = new_attacker
            fight.save()
            self.logger.info(f"Promoted {new_attacker} to attacker in fight {fight.id}")
            return True
        else:
            # No one to replace attacker, close the fight
            self._close_fight(fight, "Attacker left and no replacement available")
            return True

    def _handle_defender_leaving(self, fight: Fight) -> bool:
        """
        Handle the defender leaving the fight.
        
        Args:
            fight: Fight instance
            
        Returns:
            bool: True if defender was successfully handled
        """
        # Try to promote a pending joiner to defender
        pending_joiners = fight.pending_join.filter(is_active=True)
        if pending_joiners.exists():
            new_defender = pending_joiners.first()
            fight.pending_join.remove(new_defender)
            fight.defender = new_defender
            fight.save()
            self.logger.info(f"Promoted {new_defender} to defender in fight {fight.id}")
            return True
        else:
            # No one to replace defender, close the fight
            self._close_fight(fight, "Defender left and no replacement available")
            return True

    def _remove_pending_joiner(self, fight: Fight, character: Character):
        """
        Remove a character from pending joiners.
        
        Args:
            fight: Fight instance
            character: Character to remove from pending joiners
        """
        try:
            fight.pending_join.remove(character)
            self.logger.debug(f"Removed {character} from pending joiners for fight {fight.id}")
        except Exception as e:
            self.logger.error(f"Failed to remove {character} from pending joiners for fight {fight.id}: {e}")

    def _close_fight(self, fight: Fight, reason: str):
        """
        Close a fight with the given reason.
        
        Args:
            fight: Fight instance to close
            reason: Reason for closing the fight
        """
        try:
            fight.open = False
            fight.save()
            self.logger.info(f"Closed fight {fight.id}: {reason}")
        except Exception as e:
            self.logger.error(f"Failed to close fight {fight.id}: {e}")

    def _emit_leave_events(self, fight: Fight, character: Character):
        """
        Emit events for a character leaving the fight.
        
        Args:
            fight: Fight instance
            character: Character that left
        """
        try:
            # Emit event to all characters at the position
            self._emit_character_leave_fight_event(fight, character)

            # Emit event to the specific character
            self._emit_left_fight_event(fight, character)

        except Exception as e:
            self.logger.error(f"Failed to emit leave events for {character} leaving fight {fight.id}: {e}")

    def _emit_character_leave_fight_event(self, fight: Fight, character: Character):
        """
        Emit CharacterLeaveFight event to all characters at the position.
        
        Args:
            fight: Fight instance
            character: Character leaving
        """
        try:
            from apps.core.bus.events.fight.produced import CharacterLeaveFightEvent

            event = CharacterLeaveFightEvent.create_event(
                fight_id=fight.id,
                character_id=character.id,
                position_id=fight.position.id
            )

            self.notifier.bus.publish(event)
            self.logger.debug(f"Emitted CharacterLeaveFight event for {character} leaving fight {fight.id}")

        except ImportError:
            self.logger.warning("CharacterLeaveFightEvent not implemented yet")
        except Exception as e:
            self.logger.error(f"Failed to emit CharacterLeaveFight event: {e}")

    def _emit_left_fight_event(self, fight: Fight, character: Character):
        """
        Emit LeftFight event to the specific character.
        
        Args:
            fight: Fight instance
            character: Character leaving
        """
        try:
            from apps.core.bus.events.fight.produced import LeftFightEvent

            event = LeftFightEvent.create_event(
                fight_id=fight.id,
                character_id=character.id
            )

            self.notifier.bus.publish(event)
            self.logger.debug(f"Emitted LeftFight event for {character} leaving fight {fight.id}")

        except ImportError:
            self.logger.warning("LeftFightEvent not implemented yet")
        except Exception as e:
            self.logger.error(f"Failed to emit LeftFight event: {e}")
