"""
Unit tests for NPCFactory service.
"""

from django.test import TestCase
from django.core.management import call_command

from apps.character.models.npc import CharacterTemplate
from apps.game.services.npc.factory import NPCFactory
from apps.game.services.npc.factory.interface import NPCFactoryConfig
from apps.game.tests.factories import CampaignFactory
from apps.world.tests.factories import PositionFactory
from apps.world.models import Location


class NPCFactoryTest(TestCase):
    """Test cases for NPCFactory service."""

    fixtures = ['fixtures/test/sandbox.yaml']

    def setUp(self):
        """Set up test data."""
        # Create factory instances
        self.factory = NPCFactory()

    def test_create_npc_from_fixture_template(self):
        """Test creating NPC from the first template in fixtures."""
        # Get the first template from fixtures
        template = CharacterTemplate.objects.first()
        self.assertIsNotNone(template, "No CharacterTemplate found in fixtures")

        # Create position using factory boy with any location from fixture
        location = Location.objects.first()
        self.assertIsNotNone(location, "No Location found in fixtures")

        position = PositionFactory(sub_location__location=location)

        # Create campaign using factory boy
        campaign = CampaignFactory()

        # Create the NPC using NPCFactory
        config = NPCFactoryConfig(
            template=template,
            position=position,
            behavior=template.behavior,
            campaign=campaign
        )

        # Test NPCFactory.create_npc() method
        npc = self.factory.create_npc(config)

        # Assertions
        self.assertIsNotNone(npc, "NPC should be created")
        self.assertEqual(npc.position, position, "NPC should be at the specified position")
        self.assertEqual(npc.campaign, campaign, "NPC should belong to the specified campaign")
        self.assertEqual(npc.behavior, template.behavior, "NPC should have the template's behavior")

        # Verify NPC has template properties
        if template.name:
            self.assertIn(template.name, npc.name or "", "NPC name should be based on template")

        # Verify NPC is saved to database
        self.assertIsNotNone(npc.id, "NPC should be saved to database")

    def test_create_npc_with_specific_fixture_template(self):
        """Test creating NPC using the first CharacterTemplate from fixtures."""
        # Get the first template specifically (should be "Brick 'The Boulder' Malone")
        template = CharacterTemplate.objects.order_by('created_at').first()
        self.assertIsNotNone(template, "No CharacterTemplate found in fixtures")

        # Create position using factory boy
        position = PositionFactory()

        # Create campaign using factory boy
        campaign = CampaignFactory()

        # Create the NPC
        config = NPCFactoryConfig(
            template=template,
            position=position,
            behavior=template.behavior,
            campaign=campaign
        )

        npc = self.factory.create_npc(config)

        # Verify the NPC was created successfully
        self.assertIsNotNone(npc)
        self.assertEqual(npc.position, position)
        self.assertEqual(npc.campaign, campaign)
        self.assertTrue(npc.npc, "Character should be marked as NPC")

    def test_npc_factory_config_validation(self):
        """Test NPCFactoryConfig validation."""
        template = CharacterTemplate.objects.first()
        position = PositionFactory()
        campaign = CampaignFactory()

        # Test valid config
        config = NPCFactoryConfig(
            template=template,
            position=position,
            behavior=template.behavior,
            campaign=campaign
        )

        # Should not raise any exception
        config.validate()

        # Test config with None template (should raise exception)
        with self.assertRaises(ValueError):
            invalid_config = NPCFactoryConfig(
                template=None,
                position=position,
                behavior=template.behavior,
                campaign=campaign
            )
            invalid_config.validate()

    def test_multiple_npcs_from_same_template(self):
        """Test creating multiple NPCs from the same template."""
        template = CharacterTemplate.objects.first()
        campaign = CampaignFactory()

        npcs = []
        for i in range(3):
            position = PositionFactory()
            config = NPCFactoryConfig(
                template=template,
                position=position,
                behavior=template.behavior,
                campaign=campaign
            )
            npc = self.factory.create_npc(config)
            npcs.append(npc)

        # Verify all NPCs were created
        self.assertEqual(len(npcs), 3)

        # Verify they are different instances
        for i, npc in enumerate(npcs):
            self.assertIsNotNone(npc.id)
            for j, other_npc in enumerate(npcs):
                if i != j:
                    self.assertNotEqual(npc.id, other_npc.id)
