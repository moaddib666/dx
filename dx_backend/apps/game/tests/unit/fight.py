"""
Unit tests for Fight functionality.
"""
from functools import partial
from unittest.mock import Mock

from django.test import TestCase

from apps.action.models import CharacterAction
from apps.character.models.npc import CharacterTemplate
from apps.core.models import BehaviorModel
from apps.game.services.action.factory import ManualCharacterActionPlayerServiceFactory, CharacterActionFactory
from apps.game.services.character.core import CharacterService
from apps.game.services.fight.core import FightFactory
from apps.game.services.npc.factory import NPCFactory
from apps.game.services.npc.factory.interface import NPCFactoryConfig
from apps.game.tests.factories import CampaignFactory, OrganizationFactory
from apps.game.tests.integration.factories import CycleFactory
from apps.world.models import Location
from apps.world.tests.factories import PositionFactory


class FightTest(TestCase):
    """Test cases for Fight functionality."""

    fixtures = ['fixtures/test/sandbox.yaml']

    def setUp(self):
        """Set up test data."""
        # Create factory instances
        self.npc_factory = NPCFactory()
        self.fight_factory = FightFactory()
        self.campaign = CampaignFactory()
        # Create a cycle for the fight
        self.cycle = CycleFactory(campaign=self.campaign, number=1)

        self.auto_map_svc = Mock()  # Mocked for simplicity
        self.bargain_cleanup_svc = Mock()  # Mocked for simplicity
        self.notify = Mock()  # Mocked for simplicity

        self.character_action_factory = CharacterActionFactory()
        # Create the service instance
        self.cycle_play_svc = partial(
            ManualCharacterActionPlayerServiceFactory,
            auto_map_svc=self.auto_map_svc,  # Mocked for simplicity
            bargain_cleanup_svc=self.bargain_cleanup_svc,  # Mocked for simplicity
            notify=self.notify,  # Mocked for simplicity
            factory=self.character_action_factory,  # CharacterActionFactory instance
        )

    def _ensure_alive(self, character):
        """
        Ensure the character is alive and has action points.
        This is a helper method to check the character's state.
        """
        character.refresh_from_db()
        svc = CharacterService(character)
        svc.refill_health()
        svc.refill_energy()
        self.assertFalse(svc.is_knocked_out())

    def test_the_fight_mechanic(self):
        """
        We need to test the fight creation and fight actions between two NPCs
        - We spawn Character and NPCs in the same position
        - As the NPC is aggressive, it should attack the Character
        - The first attack must be applied in same cycle and fight must be created in the next cycle
        - The NPC must be the attacker and Character must be the defender in the fight
        - When fight is created, the character must pending join the fight and have no action points so no new actions expected
        - In the next cycle, all characters that been pending join the fight must been removed from pending joiners
        - When characters have ap it's expected that the NPC would continue attacking the Character
        - If any other characters are in the same position, does not metter on what cycle they must been pending join the fight if the fight is open and not ended thay action points are reduced to 0 and thay must wait for 1 cycle to join the fight
        - The fight ended when no affective actions are applied in the fight for 3 cycles
        - The fight must be closed when the fight ended
        """
        # Create 2 different organizations using factory boy
        organization_1 = OrganizationFactory(name="Red Dragons")
        organization_2 = OrganizationFactory(name="Blue Wolves")

        # Get existing templates from fixtures and modify them for our test
        template_base = CharacterTemplate.objects.get(pk="1790c68e-e4cd-400d-8c8e-c3d02fdfa583")
        self.assertIsNotNone(template_base, "No CharacterTemplate found in fixtures")

        # Create positions using factory boy with any location from fixture
        location = Location.objects.first()
        self.assertIsNotNone(location, "No Location found in fixtures")

        position = PositionFactory.create(sub_location__location=location)

        # Create campaign using factory boy
        campaign = self.campaign

        # Create the first NPC using NPCFactory
        template_config = NPCFactoryConfig(
            template=template_base,
            behavior=BehaviorModel.AGGRESSIVE,
            campaign=campaign,
            position=position,
        )
        character1 = self.npc_factory.create_npc(template_config)
        # Make sure the npc have schools and skills
        self.assertTrue(character1.learned_skills.exists(), "NPC 1 should have skills")
        self.assertTrue(character1.learned_schools.exists(), "NPC 1 should have schools")

        # Convert the NPC to the player character
        character1.npc = False
        character1.organization = organization_1
        character1.save(
            update_fields=['npc', 'organization']
        )
        # Create the second NPC using NPCFactory
        npc_1 = self.npc_factory.create_npc(template_config)
        npc_1.organization = organization_2
        npc_1.save()
        # Make sure the npc have schools and skills
        self.assertTrue(npc_1.learned_skills.exists(), "NPC 2 should have skills")
        self.assertTrue(npc_1.learned_schools.exists(), "NPC 2 should have schools")

        # Now i need to use player to switch to the next turn
        new_cycle = self.cycle_play_svc(self.cycle).play()
        self.assertIsNotNone(new_cycle, "New cycle should be created after playing the cycle")
        self._ensure_alive(character1)
        self._ensure_alive(npc_1)
        # Check that npc2 attacked character1 but fight is not created yet as actions are not applied yet
        actions = CharacterAction.objects.filter(
            cycle=new_cycle,
            initiator=npc_1,
            targets__in=[character1],
            performed=False,
            accepted=True,
        )
        self.assertEqual(actions.exists(), True, "NPC 2 should have attacked NPC 1 in the new cycle")
        npc_1.refresh_from_db()
        character1.refresh_from_db()
        self.assertFalse(npc_1.pending_fights.exists(),
                         "NPC 2 should not have fights pending join yet")
        self.assertFalse(character1.pending_fights.exists(),
                         "Character 1 should not have fights pending join yet")
        self.assertFalse(npc_1.fight, "NPC 2 should not be in a fight yet")
        self.assertFalse(character1.fight, "Character 1 should not be in a fight")
        # Run the next cycle
        new_cycle = self.cycle_play_svc(new_cycle).play()
        self.assertIsNotNone(new_cycle, "New cycle should be created after playing the cycle")
        self._ensure_alive(character1)
        self._ensure_alive(npc_1)
        # Check that fight is created
        npc_1.refresh_from_db()
        character1.refresh_from_db()
        self.assertTrue(npc_1.pending_fights.exists(),
                        "NPC 2 should have fights pending join after the second cycle")
        self.assertTrue(character1.pending_fights.exists(),
                        "Character 1 should have fights pending join after the second cycle")
        self.assertTrue(npc_1.fight, "NPC 2 should be in a fight after the second cycle")
        self.assertTrue(character1.fight, "Character 1 should be in a fight after the second cycle")
        self.assertEqual(npc_1.fight, character1.fight,
                         "NPC 2 and Character 1 should be in the same fight after the second cycle")
        # Check that new actions is not scheduled as connected to fight
        actions = CharacterAction.objects.filter(
            cycle=new_cycle,
            performed=False,
            accepted=True,
        )
        self.assertFalse(actions.exists(), "No new actions should be scheduled after fight creation")
        fight = npc_1.fight
        self.assertEqual(fight.attacker, npc_1, "NPC must be the attacker in the fight")
        self.assertEqual(fight.defender, character1, "Character must be the defender in the fight")
        self.assertEqual(fight.position, position, "Fight must be in the same position as the NPCs")
        self.assertTrue(fight.open, "Fight must be open after creation")
        self.assertEqual(fight.campaign, campaign, "Fight must be in the same campaign as the NPCs")

        # Play the cycle again to check fight actions
        new_cycle = self.cycle_play_svc(new_cycle).play()
        self._ensure_alive(character1)
        self._ensure_alive(npc_1)
        self.assertIsNotNone(new_cycle, "New cycle should be created after playing the cycle")
        # Check that fight actions are created
        actions = CharacterAction.objects.filter(
            cycle=new_cycle,
            fight=fight,
            performed=False,
            accepted=True,
        )
        self.assertFalse(actions.exists(), "Fight actions should be created after playing the cycle due to the fight "
                                           "pending for participants")

        # Play the cycle again to process pending joiners and check fight actions
        new_cycle = self.cycle_play_svc(new_cycle).play()
        self.assertIsNotNone(new_cycle, "New cycle should be created after playing the cycle")
        self._ensure_alive(character1)
        self._ensure_alive(npc_1)
        # Check that fight actions are created
        actions = CharacterAction.objects.filter(
            cycle=new_cycle,
            fight=fight,
            performed=False,
            accepted=True,
        )
        self.assertTrue(actions.exists(), "Fight actions should be created after playing the cycle")

        self.assertFalse(npc_1.pending_fights.exists(),
                         "NPC 2 should not have fights pending join after the third cycle")
        self.assertFalse(character1.pending_fights.exists(),
                         "Character 1 should not have fights pending join after the third cycle")

        # Spawn another character in the same position to check auto join
        character2 = self.npc_factory.create_npc(template_config)
        character2.organization = organization_1
        character2.npc = False
        character2.save(
            update_fields=['npc', 'organization']
        )
        # Spawn another NPC in the same position to check auto join
        npc_2 = self.npc_factory.create_npc(template_config)
        npc_2.organization = organization_2
        npc_2.save(
            update_fields=['organization']
        )

        # Make sure the npc have schools and skills
        self.assertTrue(character2.learned_skills.exists(), "Character 2 should have skills")
        self.assertTrue(character2.learned_schools.exists(), "Character 2 should have schools")
        # Play the cycle again to check auto join
        new_cycle = self.cycle_play_svc(new_cycle).play()
        self.assertIsNotNone(new_cycle, "New cycle should be created after playing the cycle")
        self._ensure_alive(character1)
        self._ensure_alive(npc_1)
        # Check that character2 is pending to join the fight
        character2.refresh_from_db()
        self.assertTrue(character2.pending_fights.exists(),
                        "Character 2 should have fights pending join after the fourth cycle")
        self.assertTrue(character2.fight, "Character 2 should be in the fight after the fourth cycle")
        self.assertEqual(character2.fight, fight, "Character 2 should be in the same fight as NPC 2 and Character 1")
        self.assertEqual(character2.current_active_points, 0,
                         "Character 2 should have 0 action points after joining the fight")

        npc_2.refresh_from_db()
        self.assertTrue(npc_2.pending_fights.exists(),
                        "NPC 2 should have fights pending join after the fourth cycle")
        self.assertTrue(npc_2.fight, "NPC 2 should be in the fight after the fourth cycle")
        self.assertEqual(npc_2.fight, fight, "NPC 2 should be in the same fight as NPC 2 and Character 1")
        self.assertEqual(npc_2.current_active_points, 0,
                         "NPC 2 should have 0 action points after joining the fight")
        # Check that fight actions are created
        actions = CharacterAction.objects.filter(
            cycle=new_cycle,
            fight=fight,
            performed=False,
            accepted=True,
        )
        self.assertTrue(actions.exists(), "Fight actions should be created after playing the cycle")
        # Play the cycle again to check fight actions
        new_cycle = self.cycle_play_svc(new_cycle).play()
        self._ensure_alive(character1)
        self._ensure_alive(npc_1)
        self.assertIsNotNone(new_cycle, "New cycle should be created after playing the cycle")
        # Play the cycle again to check fight actions
        new_cycle = self.cycle_play_svc(new_cycle).play()
        self.assertIsNotNone(new_cycle, "New cycle should be created after playing the cycle")
        self._ensure_alive(character1)
        self._ensure_alive(npc_1)
        # Check that fight actions are created
        actions = CharacterAction.objects.filter(
            cycle=new_cycle,
            fight=fight,
            performed=False,
            accepted=True,
        )
        self.assertTrue(actions.exists(), "Fight actions should be created after playing the cycle")
        # Check that fight is still open

        npc_1.refresh_from_db()
        svc = CharacterService(npc_1)
        svc.knock_out()
        new_cycle = self.cycle_play_svc(new_cycle).play()
        actions = CharacterAction.objects.filter(
            cycle=new_cycle,
            performed=False,
            accepted=True,
        )
        fight.refresh_from_db()
        self.assertTrue(fight.open, "Fight should be open after the fifth cycle")
        self.assertTrue(actions.exists(), "Actions should be scheduled after fight actions")
        self.assertFalse(fight.ended_at, "Fight should not be ended yet")
        npc_2.refresh_from_db()
        svc = CharacterService(npc_2)
        svc.knock_out()
        # Play the cycle again to check fight actions
        new_cycle = self.cycle_play_svc(new_cycle).play()
        self.assertIsNotNone(new_cycle, "New cycle should be created after playing the cycle")
        # Check that fight actions are created
        actions = CharacterAction.objects.filter(
            cycle=new_cycle,
            fight=fight,
            performed=False,
            accepted=True,
        )
        self.assertFalse(actions.exists(), "Fight actions should be created after playing the cycle")
        fight.refresh_from_db()
        self.assertTrue(fight.ended_at, "Fight should not be ended yet")
        self.assertEqual(fight.ended_at, new_cycle, "Fight should be ended at the current cycle")
        character1.refresh_from_db()
        self.assertFalse(character1.pending_fights.exists(),
                         "Character 1 should not have fights pending join after the sixth cycle")
        self.assertFalse(character1.fight, "Character 1 should not be in a fight after the sixth cycle")

        self.assertFalse(character2.pending_fights.exists(),
                         "Character 2 should not have fights pending join after the sixth cycle")
        self.assertFalse(character2.fight, "Character 2 should not be in a fight after the sixth cycle")
