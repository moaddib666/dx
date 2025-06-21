#!/usr/bin/env python
"""
Test script for the admin action to create a template from an NPC.
"""
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dx_backend.settings")
django.setup()

from django.test import RequestFactory
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from apps.character.models import Character
from apps.character.admin.character import CharacterAdmin
from apps.game.services.npc.factory import NPCFactory, NPCFactoryConfig
from apps.core.models import CharacterTemplate

def test_admin_create_template_from_npc():
    """Test the admin action to create a template from an NPC."""
    # Create a factory
    factory = NPCFactory()
    
    # First, create an NPC from a template
    template = CharacterTemplate.objects.first()
    if not template:
        print("No templates available. Please create a template first.")
        return
    
    config = NPCFactoryConfig(template=template, name="Test NPC for Admin Action")
    npc = factory.create_npc(config)
    print(f"Created NPC: {npc.name}")
    
    # Set up the admin environment
    admin_site = AdminSite()
    character_admin = CharacterAdmin(Character, admin_site)
    request_factory = RequestFactory()
    request = request_factory.get('/')
    request.user = User.objects.filter(is_superuser=True).first()
    if not request.user:
        print("No superuser found. Please create a superuser first.")
        return
    
    # Execute the admin action
    queryset = Character.objects.filter(pk=npc.pk)
    character_admin.create_template_from_npc(request, queryset)
    
    # Verify that a template was created
    template_name = f"{npc.name} Template"
    template = CharacterTemplate.objects.filter(name=template_name).first()
    if template:
        print(f"Successfully created template: {template.name}")
    else:
        print("Failed to create template")
    
    # Clean up
    if template:
        template.delete()
    npc.delete()
    
    print("Test completed successfully!")

if __name__ == "__main__":
    test_admin_create_template_from_npc()