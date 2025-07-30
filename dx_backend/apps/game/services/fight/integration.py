"""
Integration module for fight services with the main game loop.

This module provides the integration points for the fight system with:
- apps.game.services.action.player.ManualCharacterActionPlayerService.prepare
- apps.game.services.action.player.ManualCharacterActionPlayerService.post
"""

import logging
import typing as t

from .coordinator import FightCoordinator

if t.TYPE_CHECKING:
    from apps.action.models import Cycle
    from apps.game.services.notifier.base import BaseNotifier


class FightGameLoopIntegration:
    """
    Provides integration points for the fight system with the main game loop.
    """

    def __init__(self, notifier: "BaseNotifier"):
        self.notifier = notifier
        self.logger = logging.getLogger("game.services.fight.FightGameLoopIntegration")

    def prepare_cycle_fights(self, cycle: "Cycle") -> dict:
        """
        Prepare fight-related activities at the start of a cycle.
        
        This should be called during ManualCharacterActionPlayerService.prepare()
        
        Args:
            cycle: The current cycle being prepared
            
        Returns:
            Dict containing preparation results
        """
        self.logger.info(f"Preparing fights for cycle {cycle.number}")

        coordinator = FightCoordinator(self.notifier, cycle)
        # Process all fight activities
        results = coordinator.process_all_fights()
        # Log summary
        self._log_cycle_summary(cycle, results)
        self.logger.info(f"Prepared {len(results)} new fights for cycle {cycle.number}")

        return {
            'new_fights': results,
            'cycle': cycle.number
        }

    def post_cycle_fights(self, cycle: "Cycle") -> dict:
        """
        Process fight-related activities at the end of a cycle.
        
        This should be called during ManualCharacterActionPlayerService.post()
        
        Args:
            cycle: The current cycle being processed
            
        Returns:
            Dict containing post-processing results
        """
        self.logger.info(f"Post-processing fights for cycle {cycle.number}")

        coordinator = FightCoordinator(self.notifier, cycle)

        return {}

    def _log_cycle_summary(self, cycle: "Cycle", results: dict):
        """
        Log a summary of fight activities for the cycle.
        
        Args:
            cycle: The cycle that was processed
            results: Results from fight processing
        """
        summary_parts = []

        if results.get('detected_fights'):
            summary_parts.append(f"{len(results['detected_fights'])} new fights")

        if results.get('auto_joins'):
            total_joins = sum(len(joiners) for joiners in results['auto_joins'].values())
            summary_parts.append(f"{total_joins} auto-joins")

        if results.get('authorized_leaves'):
            total_leaves = sum(len(leavers) for leavers in results['authorized_leaves'].values())
            summary_parts.append(f"{total_leaves} authorized leaves")

        if results.get('pending_joins'):
            total_pending = sum(len(joiners) for joiners in results['pending_joins'].values())
            summary_parts.append(f"{total_pending} pending joins processed")

        if results.get('closed_fights'):
            summary_parts.append(f"{len(results['closed_fights'])} fights closed")

        if summary_parts:
            summary = ", ".join(summary_parts)
            self.logger.info(f"Cycle {cycle.number} fight summary: {summary}")
        else:
            self.logger.debug(f"Cycle {cycle.number}: No fight activities")


def integrate_with_manual_player_service():
    """
    Example of how to integrate the fight system with ManualCharacterActionPlayerService.
    
    This function shows the recommended integration pattern. You would modify
    ManualCharacterActionPlayerService to use this pattern.
    """

    # Example integration in ManualCharacterActionPlayerService.prepare():
    def prepare_with_fights(self):
        """Modified prepare method that includes fight processing."""
        # Existing prepare logic...
        self.base_stats_applier.apply()
        self.npc_actions_scheduler.schedule_actions(self.cycle)
        self.auto_map_svc.map_characters()
        self.perform_follow_chase()

        # Add fight preparation
        fight_integration = FightGameLoopIntegration(self.notify)
        fight_results = fight_integration.prepare_cycle_fights(self.cycle)

        # Store results if needed
        self.fight_preparation_results = fight_results

    # Example integration in ManualCharacterActionPlayerService.post():
    def post_with_fights(self):
        """Modified post method that includes fight processing."""
        # Existing post logic...
        self.update_characters()
        self.active_shields_cls(self.get_active_shields()).decrease_cycles()
        self.bargain_cleanup_svc.cleanup()

        # Add fight post-processing
        fight_integration = FightGameLoopIntegration(self.notify)
        fight_results = fight_integration.post_cycle_fights(self.cycle)

        # Store results if needed
        self.fight_post_results = fight_results

    return prepare_with_fights, post_with_fights
