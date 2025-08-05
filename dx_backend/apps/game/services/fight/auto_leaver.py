import logging
import typing as t

from apps.action.models import Cycle
from apps.character.models import Character
from apps.fight.models import Fight

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

    def process_auto_leave(self, cycle: "Cycle") -> dict[int, list]:
        """
        Process authorized leaving for all fights in the campaign.
        """
        all_fights = self._get_all_fights(cycle.campaign)
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
            campaign=campaign
        ).select_related('position', 'attacker', 'defender').prefetch_related('pending_joiners'))

    def _process_fight_leavers(self, fight: Fight) -> list[Character]:
        """
        Process leaving for a single fight.
        """
        leavers = []

        # Check main participants (attacker and defender)
        for character in fight.joined.all():
            if character and self._should_character_leave(fight, character):
                if self._remove_participant(fight, character):
                    leavers.append(character)
                    self._emit_leave_events(fight, character)

        return leavers

    def _should_character_leave(self, fight: Fight, character: Character) -> bool:
        """
        Determine if a character should leave the fight.
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

        return False

    def _is_fight_ending_gracefully(self, fight: Fight) -> bool:
        """
        Check if the fight is ending gracefully (e.g., through proper game mechanics).
        """
        # If fight has an end cycle, it's ending gracefully
        return fight.ended_at is not None

    def _remove_participant(self, fight: Fight, character: Character) -> bool:
        """
        Remove a main participant from the fight.
        """
        try:
            character.fight = None  # Clear the fight reference
            character.pending_fights.filter(fight=fight).delete()  # Remove any pending join records
            character.save(update_fields=['fight'])
            return True
        except Exception as e:
            self.logger.error(f"Failed to remove main participant {character} from fight {fight.id}: {e}")
            return False

    def _emit_leave_events(self, fight: Fight, character: Character):
        """
        Emit events for a character leaving the fight.
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
