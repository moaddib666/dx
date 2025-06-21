#!/usr/bin/env python
"""
Test script to verify the fix for the IntegrityError in create_template_from_npc.
This script creates an NPC, adds a school to it, and then creates a template from the NPC
multiple times to ensure no IntegrityError occurs.
"""
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dx_backend.settings")
django.setup()

from apps.character.models import Character, CharacterTemplate
from apps.game.services.npc.factory import NPCFactory, NPCFactoryConfig
from apps.skills.models import LearnedSchool
from apps.character.models.player import StatModifier
from apps.items.models import Item, WorldItem, CharacterItem
from apps.core.models import CharacterStats

def test_template_from_npc_fix():
    """Test that creating a template from an NPC multiple times doesn't cause IntegrityError."""
    # Create a factory
    factory = NPCFactory()
    
    # First, create an NPC from a template
    template = CharacterTemplate.objects.first()
    if not template:
        print("No templates available. Please create a template first.")
        return
    
    config = NPCFactoryConfig(template=template, name="Test NPC for Fix")
    npc = factory.create_npc(config)
    print(f"Created NPC: {npc.name}")
    
    # Add a school to the NPC
    try:
        from apps.school.models import School
        school = School.objects.first()
        if school:
            LearnedSchool.objects.create(
                character=npc,
                school=school,
                is_base=True
            )
            print(f"Added school: {school.name} to NPC")
    except Exception as e:
        print(f"Could not add school: {e}")
    
    # Create a template from the NPC
    template_name = "Test Template from NPC Fix"
    new_template = factory.create_template_from_npc(npc, template_name)
    print(f"Created template: {new_template.name}")
    
    # Create a template from the NPC again (this would previously cause an IntegrityError)
    try:
        new_template2 = factory.create_template_from_npc(npc, template_name + " 2")
        print(f"Created second template: {new_template2.name}")
        
        # Create a template from the NPC a third time
        new_template3 = factory.create_template_from_npc(npc, template_name + " 3")
        print(f"Created third template: {new_template3.name}")
        
        print("Test passed: No IntegrityError occurred when creating multiple templates from the same NPC")
    except Exception as e:
        print(f"Test failed: {e}")
    
    # Clean up
    try:
        if 'new_template3' in locals():
            new_template3.delete()
        if 'new_template2' in locals():
            new_template2.delete()
        new_template.delete()
        npc.delete()
    except Exception as e:
        print(f"Error during cleanup: {e}")
    
    print("Test completed")

if __name__ == "__main__":
    test_template_from_npc_fix()