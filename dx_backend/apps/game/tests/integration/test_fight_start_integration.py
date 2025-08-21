"""
Integration tests for ManualCharacterActionPlayerService and FightGameLoopIntegration.

These tests verify how fights start when the game loop processes cycles.
"""

from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase, override_settings

from apps.action.models import Cycle
from apps.character.models import Character
from apps.game.services.action.player import ManualCharacterActionPlayerService
from apps.game.services.fight.integration import FightGameLoopIntegration
from .factories import CampaignFactory, CycleFactory, CharacterActionFactory


class FightStartIntegrationTest(TestCase):
    """Test how fights start through the integration of ManualCharacterActionPlayerService and FightGameLoopIntegration."""

    def setUp(self):
        """Set up test dependencies and mocks."""
        # Create real Campaign and Cycle objects using factories
        self.campaign = CampaignFactory()
        self.cycle = CycleFactory(campaign=self.campaign, number=1)

        # Mock all the dependencies for ManualCharacterActionPlayerService
        self.factory = Mock()
        self.effects_apply_factory = Mock()
        self.effects_manager_factory = Mock()
        self.auto_map_svc = Mock()
        self.bargain_cleanup_svc = Mock()
        self.notify = Mock()

        # Create the service instance
        self.player_service = ManualCharacterActionPlayerService(
            cycle=self.cycle,
            factory=self.factory,
            effects_apply_factory=self.effects_apply_factory,
            effects_manager_factory=self.effects_manager_factory,
            auto_map_svc=self.auto_map_svc,
            bargain_cleanup_svc=self.bargain_cleanup_svc,
            notify=self.notify
        )

    def test_fight_integration_initialization(self):
        """Test that FightGameLoopIntegration is properly initialized in ManualCharacterActionPlayerService."""
        # Verify that fight_integration is created
        self.assertIsInstance(self.player_service.fight_integration, FightGameLoopIntegration)
        self.assertEqual(self.player_service.fight_integration.notifier, self.notify)

    @patch('apps.game.services.fight.integration.FightCoordinator')
    @patch('apps.character.models.Character.objects.filter')
    def test_prepare_cycle_fights_called_during_prepare(self, mock_char_filter, mock_coordinator_class):
        """Test that prepare_cycle_fights is called during the prepare phase."""
        # Mock the coordinator and its methods
        mock_coordinator = Mock()
        mock_coordinator.process_all_fights.return_value = {
            'detected_fights': [],
            'auto_joins': {},
            'authorized_leaves': {},
            'pending_joins': {},
            'closed_fights': []
        }
        mock_coordinator_class.return_value = mock_coordinator

        # Mock Character.objects.filter to return empty queryset
        mock_char_filter.return_value = []

        # Mock other dependencies
        with patch.object(self.player_service.base_stats_applier, 'apply'), \
                patch.object(self.player_service.auto_map_svc, 'map_characters'), \
                patch.object(self.player_service, 'perform_follow_chase'), \
                patch.object(self.player_service.npc_actions_scheduler, 'schedule_actions'):
            new_cycle = CycleFactory(campaign=self.campaign, number=2)

            # Call prepare
            self.player_service.prepare(new_cycle)

            # Verify that FightCoordinator was created with correct parameters
            mock_coordinator_class.assert_called_once_with(self.notify, new_cycle)

            # Verify that process_all_fights was called
            mock_coordinator.process_all_fights.assert_called_once()

            # Verify that fight_preparation_results is stored
            self.assertIsNotNone(self.player_service.fight_preparation_results)
            self.assertEqual(self.player_service.fight_preparation_results['cycle'], 2)

    @patch('apps.game.services.fight.integration.FightCoordinator')
    def test_post_cycle_fights_called_during_post(self, mock_coordinator_class):
        """Test that post_cycle_fights is called during the post phase."""
        # Mock the coordinator
        mock_coordinator = Mock()
        mock_coordinator_class.return_value = mock_coordinator

        # Mock other dependencies
        with patch.object(self.player_service, 'update_characters'), \
                patch.object(self.player_service, 'get_active_shields') as mock_get_shields, \
                patch.object(self.player_service.bargain_cleanup_svc, 'cleanup'):
            mock_get_shields.return_value = []

            # Call post
            self.player_service.post()

            # Verify that FightCoordinator was created with correct parameters
            mock_coordinator_class.assert_called_once_with(self.notify, self.cycle)

    @patch('apps.game.services.fight.integration.FightCoordinator')
    def test_fight_detection_results_in_prepare(self, mock_coordinator_class):
        """Test that fight detection results are properly handled in prepare phase."""
        # Mock detected fights
        detected_fights = [
            {'fight_id': 1, 'participants': ['char1', 'char2']},
            {'fight_id': 2, 'participants': ['char3', 'char4']}
        ]

        mock_coordinator = Mock()
        mock_coordinator.process_all_fights.return_value = {
            'detected_fights': detected_fights,
            'auto_joins': {'fight_1': ['char5']},
            'authorized_leaves': {},
            'pending_joins': {'fight_2': ['char6']},
            'closed_fights': []
        }
        mock_coordinator_class.return_value = mock_coordinator

        # Mock other dependencies
        with patch.object(self.player_service.base_stats_applier, 'apply'), \
                patch.object(self.player_service.auto_map_svc, 'map_characters'), \
                patch.object(self.player_service, 'perform_follow_chase'), \
                patch.object(self.player_service.npc_actions_scheduler, 'schedule_actions'):
            new_cycle = CycleFactory(campaign=self.campaign, number=3)

            # Call prepare
            self.player_service.prepare(new_cycle)

            # Verify that the results contain detected fights
            results = self.player_service.fight_preparation_results
            self.assertEqual(len(results['new_fights']['detected_fights']), 2)
            self.assertEqual(results['new_fights']['detected_fights'], detected_fights)
            self.assertIn('fight_1', results['new_fights']['auto_joins'])
            self.assertIn('fight_2', results['new_fights']['pending_joins'])

    def test_fight_integration_standalone_prepare_cycle_fights(self):
        """Test FightGameLoopIntegration.prepare_cycle_fights method standalone."""
        fight_integration = FightGameLoopIntegration(self.notify)

        with patch('apps.game.services.fight.integration.FightCoordinator') as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator.process_all_fights.return_value = {
                'detected_fights': [{'fight_id': 1}],
                'auto_joins': {},
                'authorized_leaves': {},
                'pending_joins': {},
                'closed_fights': []
            }
            mock_coordinator_class.return_value = mock_coordinator

            # Call the method
            result = fight_integration.prepare_cycle_fights(self.cycle)

            # Verify coordinator was created and called
            mock_coordinator_class.assert_called_once_with(self.notify, self.cycle)
            mock_coordinator.process_all_fights.assert_called_once()

            # Verify result structure
            self.assertIn('new_fights', result)
            self.assertIn('cycle', result)
            self.assertEqual(result['cycle'], self.cycle.number)
            self.assertEqual(len(result['new_fights']['detected_fights']), 1)

    def test_fight_integration_standalone_post_cycle_fights(self):
        """Test FightGameLoopIntegration.post_cycle_fights method standalone."""
        fight_integration = FightGameLoopIntegration(self.notify)

        with patch('apps.game.services.fight.integration.FightCoordinator') as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator_class.return_value = mock_coordinator

            # Call the method
            result = fight_integration.post_cycle_fights(self.cycle)

            # Verify coordinator was created
            mock_coordinator_class.assert_called_once_with(self.notify, self.cycle)

            # Verify result is a dict (even if empty for now)
            self.assertIsInstance(result, dict)

    @patch('apps.game.services.fight.integration.FightCoordinator')
    def test_fight_start_sequence_integration(self, mock_coordinator_class):
        """Test the complete fight start sequence through prepare -> play -> post cycle."""
        # Mock fight detection in prepare phase
        mock_coordinator = Mock()
        mock_coordinator.process_all_fights.return_value = {
            'detected_fights': [{'fight_id': 1, 'started': True}],
            'auto_joins': {},
            'authorized_leaves': {},
            'pending_joins': {},
            'closed_fights': []
        }
        mock_coordinator_class.return_value = mock_coordinator

        # Mock Cycle.objects.next to return a new cycle
        with patch('apps.action.models.Cycle.objects.next') as mock_next_cycle, \
                patch.object(self.player_service, '_play'), \
                patch.object(self.player_service, 'update_characters'), \
                patch.object(self.player_service, 'get_active_shields') as mock_get_shields, \
                patch.object(self.player_service.base_stats_applier, 'apply'), \
                patch.object(self.player_service.auto_map_svc, 'map_characters'), \
                patch.object(self.player_service, 'perform_follow_chase'), \
                patch.object(self.player_service.npc_actions_scheduler, 'schedule_actions'), \
                patch.object(self.player_service.bargain_cleanup_svc, 'cleanup'):
            next_cycle = Mock(spec=Cycle)
            next_cycle.number = 2
            next_cycle.campaign = self.cycle.campaign
            mock_next_cycle.return_value = next_cycle
            mock_get_shields.return_value = []

            # Call play (which calls prepare and post)
            result_cycle = self.player_service.play()

            # Verify the sequence
            # 1. post() was called (fight post-processing)
            # 2. prepare() was called with next cycle (fight preparation)
            # 3. Notifier was called for new cycle
            self.notify.new_cycle.assert_called_once_with(next_cycle)

            # Verify fight preparation results were stored
            self.assertIsNotNone(self.player_service.fight_preparation_results)
            self.assertEqual(len(self.player_service.fight_preparation_results['new_fights']['detected_fights']), 1)

            # Verify the returned cycle
            self.assertEqual(result_cycle, next_cycle)

    def test_fight_integration_logging(self):
        """Test that fight integration properly logs fight activities."""
        fight_integration = FightGameLoopIntegration(self.notify)

        with patch('apps.game.services.fight.integration.FightCoordinator') as mock_coordinator_class, \
                patch.object(fight_integration.logger, 'info') as mock_log_info:
            mock_coordinator = Mock()
            mock_coordinator.process_all_fights.return_value = {
                'detected_fights': [{'fight_id': 1}],
                'auto_joins': {},
                'authorized_leaves': {},
                'pending_joins': {},
                'closed_fights': []
            }
            mock_coordinator_class.return_value = mock_coordinator

            # Call prepare_cycle_fights
            fight_integration.prepare_cycle_fights(self.cycle)

            # Verify logging calls
            mock_log_info.assert_any_call(f"Preparing fights for cycle {self.cycle.number}")
            mock_log_info.assert_any_call(f"Prepared 1 new fights for cycle {self.cycle.number}")

    def test_real_actions_with_database_models(self):
        """Test that real CharacterAction objects work with factory-created Cycle and Campaign."""
        # Create some real CharacterAction objects for this cycle
        action1 = CharacterActionFactory(cycle=self.cycle, accepted=True, performed=False, order=1.0)
        action2 = CharacterActionFactory(cycle=self.cycle, accepted=True, performed=False, order=2.0)
        action3 = CharacterActionFactory(cycle=self.cycle, accepted=False, performed=False, order=3.0)

        # Verify the actions are properly linked to the cycle
        self.assertEqual(action1.cycle, self.cycle)
        self.assertEqual(action2.cycle, self.cycle)
        self.assertEqual(action3.cycle, self.cycle)

        # Verify the cycle has the actions
        all_actions = self.cycle.actions.all()
        self.assertEqual(len(all_actions), 3)

        # Test the get_actions method which filters for accepted=True, performed=False
        accepted_actions = self.cycle.actions.filter(performed=False, accepted=True).order_by("order")
        self.assertEqual(len(accepted_actions), 2)
        self.assertEqual(list(accepted_actions), [action1, action2])

        # Verify campaign relationship works through cycle
        self.assertEqual(action1.cycle.campaign, self.campaign)
        self.assertEqual(action2.cycle.campaign, self.campaign)

        # Test action state changes
        action1.perform()
        action1.refresh_from_db()
        self.assertTrue(action1.performed)

        # After performing action1, only action2 should be in the accepted/not performed list
        remaining_actions = self.cycle.actions.filter(performed=False, accepted=True).order_by("order")
        self.assertEqual(len(remaining_actions), 1)
        self.assertEqual(remaining_actions[0], action2)
