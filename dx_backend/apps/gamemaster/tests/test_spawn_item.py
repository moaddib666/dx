import uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.items.models import Item, WorldItem, CharacterItem
from apps.character.models import Character
from apps.world.models import Position, Dimension


class SpawnItemTests(TestCase):
    """
    Test cases for the spawn_item endpoint.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        # Create a test item
        self.item = Item.objects.create(
            name="Test Item",
            description="A test item",
            type="misc",
            charges=1,
            weight=1.0,
            visibility=1.0,
            base_price=10
        )
        
        # Create a test dimension
        self.dimension = Dimension.objects.create(
            id=1,
            speed=1.0,
            energy=1.0
        )
        
        # Create a test position
        self.position = Position.objects.create(
            id=uuid.uuid4(),
            grid_x=0,
            grid_y=0,
            grid_z=0,
            sub_location_id=1  # Assuming a sub_location with ID 1 exists
        )
        
        # Create a test character
        self.character = Character.objects.create(
            name="Test Character",
            position=self.position,
            dimension=self.dimension,
            owner_id=1  # Assuming a client with ID 1 exists
        )
        
        # Set up the API client
        self.client = APIClient()
        self.client.force_authenticate(user=None)  # Authenticate as admin user
        
        # URL for the spawn_item endpoint
        self.url = reverse('gamemaster-item-spawn-item', args=[self.item.id])
    
    def test_spawn_item_with_character(self):
        """
        Test spawning an item with a character ID.
        """
        data = {
            'to_character_id': str(self.character.gameobject_ptr_id)
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorldItem.objects.count(), 1)
        self.assertEqual(CharacterItem.objects.count(), 1)
        
        # Verify the item is assigned to the character
        character_item = CharacterItem.objects.first()
        self.assertEqual(character_item.character, self.character)
    
    def test_spawn_item_with_position(self):
        """
        Test spawning an item with a position ID.
        """
        data = {
            'to_position_id': str(self.position.id)
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorldItem.objects.count(), 1)
        self.assertEqual(CharacterItem.objects.count(), 0)
        
        # Verify the item is placed at the position
        world_item = WorldItem.objects.first()
        self.assertEqual(world_item.position, self.position)
    
    def test_spawn_item_with_both(self):
        """
        Test spawning an item with both character ID and position ID.
        """
        # Create another position
        another_position = Position.objects.create(
            id=uuid.uuid4(),
            grid_x=1,
            grid_y=1,
            grid_z=1,
            sub_location_id=1  # Assuming a sub_location with ID 1 exists
        )
        
        data = {
            'to_character_id': str(self.character.gameobject_ptr_id),
            'to_position_id': str(another_position.id)
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorldItem.objects.count(), 1)
        self.assertEqual(CharacterItem.objects.count(), 1)
        
        # Verify the item is assigned to the character and placed at the specified position
        world_item = WorldItem.objects.first()
        self.assertEqual(world_item.position, None)  # Position should be None when picked by character
        
        character_item = CharacterItem.objects.first()
        self.assertEqual(character_item.character, self.character)
        self.assertEqual(character_item.world_item, world_item)
    
    def test_spawn_item_without_params(self):
        """
        Test spawning an item without any parameters.
        """
        data = {}
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WorldItem.objects.count(), 0)
        self.assertEqual(CharacterItem.objects.count(), 0)