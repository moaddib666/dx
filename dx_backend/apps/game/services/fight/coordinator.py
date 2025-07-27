import logging
import typing as t

from .detector import FightDetector
from .auto_joiner import FightAutoJoiner
from .auto_leaver import FightAutoLeaver
from .pending_joiner import FightPendingJoiner
from .fight_closer import FightCloser

if t.TYPE_CHECKING:
    from apps.action.models import Cycle
    from apps.game.services.notifier.base import BaseNotifier


class FightCoordinator:
    """
    Coordinates all fight-related services to manage the complete fight lifecycle.
    
    This service orchestrates:
    1. Fight detection and creation
    2. Auto-joining characters to fights
    3. Managing pending joiners
    4. Handling authorized leavers
    5. Closing finished fights
    """

    def __init__(self, notifier: "BaseNotifier", cycle: "Cycle"):
        self.notifier = notifier
        self.cycle = cycle
        self.logger = logging.getLogger("game.services.fight.FightCoordinator")

        # Initialize all fight services
        self.detector = FightDetector(notifier, cycle)
        self.auto_joiner = FightAutoJoiner(notifier)
        self.auth_leaver = FightAutoLeaver(notifier)
        self.pending_joiner = FightPendingJoiner(notifier)
        self.fight_closer = FightCloser(notifier, cycle)

    def process_all_fights(self) -> dict:
        """
        Process all fight-related activities for the current cycle.
        
        Returns:
            Dict containing results from all fight operations
        """
        self.logger.info(f"Processing all fights for cycle {self.cycle.number}")

        results = {
            'detected_fights': [],
            'auto_joins': {},
            'authorized_leaves': {},
            'pending_joins': {},
            'closed_fights': []
        }

        try:
            # 1. Detect and create new fights from aggressive actions
            results['detected_fights'] = self.detector.detect_fights()
            self.logger.debug(f"Detected {len(results['detected_fights'])} new fights")

            # 2. Handle authorized leavers (characters who should leave fights)
            results['authorized_leaves'] = self.auth_leaver.process_authorized_leavers(self.cycle.campaign)
            self.logger.debug(f"Processed authorized leavers for {len(results['authorized_leaves'])} fights")

            # 3. Process auto-joining (add characters at fight positions to pending)
            results['auto_joins'] = self.auto_joiner.process_auto_joins(self.cycle.campaign)
            self.logger.debug(f"Processed auto-joins for {len(results['auto_joins'])} fights")

            # 4. Convert pending joiners to active participants
            results['pending_joins'] = self.pending_joiner.process_pending_joiners(self.cycle.campaign)
            self.logger.debug(f"Processed pending joiners for {len(results['pending_joins'])} fights")

            # 5. Close fights that should end
            results['closed_fights'] = self.fight_closer.process_fight_endings()
            self.logger.debug(f"Closed {len(results['closed_fights'])} fights")

            self.logger.info(f"Completed fight processing for cycle {self.cycle.number}")

        except Exception as e:
            self.logger.error(f"Error during fight processing: {e}", exc_info=True)

        return results

    def process_fight_detection_only(self) -> list:
        """
        Only process fight detection (useful for specific scenarios).
        
        Returns:
            List of newly detected fights
        """
        return self.detector.detect_fights()

    def process_fight_cleanup_only(self) -> dict:
        """
        Only process fight cleanup (leavers and closers).
        
        Returns:
            Dict containing cleanup results
        """
        results = {
            'authorized_leaves': self.auth_leaver.process_authorized_leavers(self.cycle.campaign),
            'closed_fights': self.fight_closer.process_fight_endings()
        }
        return results

    def get_fight_statistics(self) -> dict:
        """
        Get statistics about fights in the current campaign.
        
        Returns:
            Dict containing fight statistics
        """
        from apps.fight.models import Fight

        stats = {
            'total_fights': Fight.objects.filter(position__campaign=self.cycle.campaign).count(),
            'active_fights': Fight.objects.filter(
                position__campaign=self.cycle.campaign,
                open=True
            ).count(),
            'fights_this_cycle': Fight.objects.filter(
                created=self.cycle
            ).count(),
            'fights_ended_this_cycle': Fight.objects.filter(
                ended_at=self.cycle
            ).count()
        }

        return stats
