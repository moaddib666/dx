import logging

from django.db.models import OuterRef, Exists

from apps.character.models import Character
from ..npc.bahavior_factory import BehaviorFactory


class NpcActionScheduler:
    def __init__(self, factory: BehaviorFactory):
        self.factory = factory

    logger = logging.getLogger("game.service.action.npcScheduler")

    def get_active_npcs(self) -> [Character]:
        """
        Retrieve all active NPCs meeting the criteria:
        1. Must be active (`is_active=True`).
        2. Must be flagged as NPC (`npc=True`).
        3. Must have a position (`position` is not null).
        4. The position must include at least one player character (`npc=False`).
        """
        # Step 1: Filter active NPCs with a valid position
        players_in_position = Character.objects.filter(
            npc=False,
            is_active=True,
            position=OuterRef('position')
        )
        active_npcs_with_players = Character.objects.filter(
            is_active=True,
            npc=True,
            position__isnull=False
        ).annotate(
            has_players=Exists(players_in_position)
        ).filter(has_players=True)

        return active_npcs_with_players

    def schedule_actions(self):
        """
        Schedule NPC actions.
        """
        for npc in self.get_active_npcs():
            logging.debug(f"Scheduling action for NPC {npc}")
            try:
                behavior = self.factory.get(npc)
                behavior.behave()
            except Exception as e:
                self.logger.error(f"Error scheduling action for NPC {npc}: {e}")
                continue
            else:
                self.logger.debug(f"Action scheduled for NPC {npc}")
