#!/usr/bin/env python
"""
Test script for creating a template from an NPC.
"""
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dx_backend.settings")
django.setup()

from apps.character.models import Character
from apps.game.services.npc.factory import NPCFactory, NPCFactoryConfig
from apps.core.models import CharacterTemplate

def test_create_template_from_npc():
    """Test creating a template from an NPC."""
    # Create a factory
    factory = NPCFactory()
    
    # First, create an NPC from a template
    # For this test, we'll use the first available template
    template = CharacterTemplate.objects.first()
    if not template:
        print("No templates available. Please create a template first.")
        return
    
    config = NPCFactoryConfig(template=template, name="Test NPC")
    npc = factory.create_npc(config)
    print(f"Created NPC: {npc.name}")
    
    # Now create a template from the NPC
    new_template = factory.create_template_from_npc(npc, "Test Template from NPC")
    print(f"Created template: {new_template.name}")
    
    # Finally, create a new NPC from the new template
    new_config = NPCFactoryConfig(template=new_template, name="New Test NPC")
    new_npc = factory.create_npc(new_config)
    print(f"Created new NPC from template: {new_npc.name}")
    
    # Clean up
    new_npc.delete()
    new_template.delete()
    npc.delete()
    
    print("Test completed successfully!")

if __name__ == "__main__":
    test_create_template_from_npc()