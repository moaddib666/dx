#!/usr/bin/env python
"""
Test script for creating a complete template from an NPC.
This script tests that schools, modifiers, and items are properly copied to the template.
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

def test_create_template_from_npc_complete():
    """Test creating a complete template from an NPC with schools, modifiers, and items."""
    # Create a factory
    factory = NPCFactory()
    
    # First, create an NPC from a template
    template = CharacterTemplate.objects.first()
    if not template:
        print("No templates available. Please create a template first.")
        return
    
    config = NPCFactoryConfig(template=template, name="Test NPC for Complete Template")
    npc = factory.create_npc(config)
    print(f"Created NPC: {npc.name}")
    
    # Add a school to the NPC
    school = None
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
    
    # Add a stat modifier to the NPC
    try:
        StatModifier.objects.create(
            character=npc,
            name=CharacterStats.PHYSICAL_STRENGTH,
            value=5
        )
        print(f"Added stat modifier: {CharacterStats.PHYSICAL_STRENGTH} +5 to NPC")
    except Exception as e:
        print(f"Could not add stat modifier: {e}")
    
    # Add an item to the NPC
    item = None
    world_item = None
    try:
        item = Item.objects.first()
        if item:
            world_item = WorldItem.objects.create(
                item=item,
                charges_left=1,
                visibility=1.0
            )
            CharacterItem.objects.create(
                character=npc,
                world_item=world_item
            )
            print(f"Added item: {item.name} to NPC")
    except Exception as e:
        print(f"Could not add item: {e}")
    
    # Now create a template from the NPC
    new_template = factory.create_template_from_npc(npc, "Test Complete Template from NPC")
    print(f"Created template: {new_template.name}")
    
    # Verify that the template has the expected schools, modifiers, and items
    school_templates = new_template.school_templates.all()
    print(f"Template has {school_templates.count()} school templates")
    for school_template in school_templates:
        print(f"  - School: {school_template.school.name}, Is Base: {school_template.is_base}")
    
    modifier_templates = new_template.modifier_templates.all()
    print(f"Template has {modifier_templates.count()} modifier templates")
    for modifier_template in modifier_templates:
        print(f"  - Stat: {modifier_template.stat}, Value: {modifier_template.value}")
    
    equipment_templates = new_template.equipment_templates.all()
    print(f"Template has {equipment_templates.count()} equipment templates")
    for equipment_template in equipment_templates:
        print(f"  - Item: {equipment_template.item.name}, Quantity: {equipment_template.quantity}")
    
    # Finally, create a new NPC from the new template
    new_config = NPCFactoryConfig(template=new_template, name="New Test NPC from Complete Template")
    new_npc = factory.create_npc(new_config)
    print(f"Created new NPC from template: {new_npc.name}")
    
    # Verify that the new NPC has the expected schools, modifiers, and items
    learned_schools = new_npc.learned_schools.all()
    print(f"New NPC has {learned_schools.count()} learned schools")
    for learned_school in learned_schools:
        print(f"  - School: {learned_school.school.name}, Is Base: {learned_school.is_base}")
    
    stat_modifiers = new_npc.stats_modifiers.all()
    print(f"New NPC has {stat_modifiers.count()} stat modifiers")
    for stat_modifier in stat_modifiers:
        print(f"  - Stat: {stat_modifier.name}, Value: {stat_modifier.value}")
    
    equipped_items = new_npc.equipped_items.all()
    print(f"New NPC has {equipped_items.count()} equipped items")
    for equipped_item in equipped_items:
        print(f"  - Item: {equipped_item.world_item.item.name}")
    
    # Clean up
    if world_item:
        world_item.delete()
    new_npc.delete()
    new_template.delete()
    npc.delete()
    
    print("Test completed successfully!")

if __name__ == "__main__":
    test_create_template_from_npc_complete()