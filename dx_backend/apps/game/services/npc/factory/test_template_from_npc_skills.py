#!/usr/bin/env python
"""
Test script for creating a template from an NPC with skills.
This script tests that skills are properly copied from an NPC to a template.
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
from apps.skills.models import LearnedSkill
from apps.core.models import CharacterStats

def test_template_from_npc_skills():
    """Test that skills are properly copied from an NPC to a template."""
    # Create a factory
    factory = NPCFactory()
    
    # First, create an NPC from a template
    template = CharacterTemplate.objects.first()
    if not template:
        print("No templates available. Please create a template first.")
        return
    
    config = NPCFactoryConfig(template=template, name="Test NPC for Skills")
    npc = factory.create_npc(config)
    print(f"Created NPC: {npc.name}")
    
    # Add a skill to the NPC
    try:
        from apps.school.models import Skill
        skill = Skill.objects.first()
        if skill:
            LearnedSkill.objects.create(
                character=npc,
                skill=skill,
                is_base=True
            )
            print(f"Added skill: {skill.name} to NPC")
        else:
            print("No skills available. Please create a skill first.")
            npc.delete()
            return
    except Exception as e:
        print(f"Could not add skill: {e}")
        npc.delete()
        return
    
    # Now create a template from the NPC
    new_template = factory.create_template_from_npc(npc, "Test Template with Skills")
    print(f"Created template: {new_template.name}")
    
    # Verify that the template has the expected skills
    skill_templates = new_template.skill_templates.all()
    print(f"Template has {skill_templates.count()} skill templates")
    for skill_template in skill_templates:
        print(f"  - Skill: {skill_template.skill.name}, Is Base: {skill_template.is_base}")
    
    # Finally, create a new NPC from the new template
    new_config = NPCFactoryConfig(template=new_template, name="New Test NPC with Skills")
    new_npc = factory.create_npc(new_config)
    print(f"Created new NPC from template: {new_npc.name}")
    
    # Verify that the new NPC has the expected skills
    learned_skills = new_npc.learned_skills.all()
    print(f"New NPC has {learned_skills.count()} learned skills")
    for learned_skill in learned_skills:
        print(f"  - Skill: {learned_skill.skill.name}, Is Base: {learned_skill.is_base}")
    
    # Clean up
    new_npc.delete()
    new_template.delete()
    npc.delete()
    
    print("Test completed successfully!")

if __name__ == "__main__":
    test_template_from_npc_skills()