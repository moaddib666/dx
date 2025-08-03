"""
Unit tests for Fight functionality.
"""
from unittest.mock import Mock

from django.test import TestCase

from apps.character.models.npc import CharacterTemplate
from apps.core.models import BehaviorModel
from apps.game.services.action.factory import ManualCharacterActionPlayerServiceFactory, CharacterActionFactory
from apps.game.services.fight.core import FightFactory
from apps.game.services.npc.factory import NPCFactory
from apps.game.services.npc.factory.interface import NPCFactoryConfig
from apps.game.tests.factories import CampaignFactory, OrganizationFactory, CharacterTemplateFactory
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
        self.cycle_play_svc = ManualCharacterActionPlayerServiceFactory(
            cycle=self.cycle,
            auto_map_svc=self.auto_map_svc,  # Mocked for simplicity
            bargain_cleanup_svc=self.bargain_cleanup_svc,  # Mocked for simplicity
            notify=self.notify,  # Mocked for simplicity
            factory=self.character_action_factory,  # CharacterActionFactory instance
        )

    def test_create_fight_between_aggressive_npcs_from_different_organizations(self):
        """Test creating a fight between 2 aggressive NPCs from different organizations."""
        # Create 2 different organizations using factory boy
        organization_1 = OrganizationFactory(name="Red Dragons")
        organization_2 = OrganizationFactory(name="Blue Wolves")

        # Get existing templates from fixtures and modify them for our test
        template_base = CharacterTemplate.objects.get(pk="1790c68e-e4cd-400d-8c8e-c3d02fdfa583")
        self.assertIsNotNone(template_base, "No CharacterTemplate found in fixtures")

        # Create 2 aggressive NPC templates from different organizations
        template_1 = CharacterTemplateFactory(
            name="Red Dragon Warrior",
            organization=organization_1,
            behavior=BehaviorModel.AGGRESSIVE,
            rank=template_base.rank,  # Use existing rank from fixture
            dimension=template_base.dimension,  # Use existing dimension from fixture
            stats_template=template_base.stats_template,  # Use existing stats template
            biography_template=template_base.biography_template  # Use existing biography template
        )
        template_2 = CharacterTemplateFactory(
            name="Blue Wolf Fighter",
            organization=organization_2,
            behavior=BehaviorModel.AGGRESSIVE,
            rank=template_base.rank,  # Use existing rank from fixture
            dimension=template_base.dimension,  # Use existing dimension from fixture
            stats_template=template_base.stats_template,  # Use existing stats template
            biography_template=template_base.biography_template  # Use existing biography template
        )

        # Create positions using factory boy with any location from fixture
        location = Location.objects.first()
        self.assertIsNotNone(location, "No Location found in fixtures")

        position = PositionFactory(sub_location__location=location)

        # Create campaign using factory boy
        campaign = self.campaign

        # Create the first NPC using NPCFactory
        config_1 = NPCFactoryConfig(
            template=template_1,
            behavior=template_1.behavior,
            campaign=campaign,
            position=position,
        )
        npc_1 = self.npc_factory.create_npc(config_1)
        # Make sure the npc hace schools and skills
        self.assertTrue(npc_1.learned_skills.exists(), "NPC 1 should have skills")
        self.assertTrue(npc_1.learned_schools.exists(), "NPC 1 should have schools")

        # Convert the NPC to the player character
        npc_1.npc = False
        npc_1.save()
        # Create the second NPC using NPCFactory
        config_2 = NPCFactoryConfig(
            template=template_2,
            position=position,
            behavior=template_2.behavior,
            campaign=campaign
        )
        npc_2 = self.npc_factory.create_npc(config_2)
        # Make sure the npc hace schools and skills
        self.assertTrue(npc_2.learned_skills.exists(), "NPC 2 should have skills")
        self.assertTrue(npc_2.learned_schools.exists(), "NPC 2 should have schools")

        # Now i need to use player to switch to the next turn
        new_cycle = self.cycle_play_svc.play()
        self.assertIsNotNone(new_cycle, "New cycle should be created after playing the cycle")
