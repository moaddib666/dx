# NPC Factory module
# This module provides a factory for creating NPCs based on templates and customization parameters.

from .api import create_npc, create_npcs
from .interface import NPCFactoryConfig, NPCFactoryProtocol
from .default import NPCFactory

__all__ = ['create_npc', 'create_npcs', 'NPCFactoryConfig', 'NPCFactoryProtocol', 'NPCFactory']
