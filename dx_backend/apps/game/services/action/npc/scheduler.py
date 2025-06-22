import logging
import typing as t
from collections import defaultdict

from django.db.models import OuterRef, Exists

from apps.character.models import Character
from apps.game.services.action.npc.behavior import DefaultBehaviorPattern
from apps.game.services.action.npc.position import PositionCharactersBehaviorStateService
from apps.game.services.npc.bahavior_factory import BehaviorFactory

if t.TYPE_CHECKING:
    from apps.world.models import Position
    from apps.character.models import Organization


class NpcActionScheduler:
    def __init__(self, factory: BehaviorFactory):
        self.factory = factory

    logger = logging.getLogger("game.service.action.npcScheduler")

    def get_active_characters(self) -> t.Dict["Position", t.Dict["Organization", t.List["Character"]]]:
        """
        Version that uses actual Position and Organization model instances as keys.
        """
        players_in_position = Character.objects.filter(
            npc=False,
            is_active=True,
            position=OuterRef('position')
        )

        active_npcs = Character.objects.filter(
            is_active=True,
            position__isnull=False
        ).annotate(
            has_players=Exists(players_in_position)
        ).filter(
            has_players=True
        ).select_related('position', 'organization').order_by('position', 'organization', 'id')

        # Group by actual model instances
        result = defaultdict(lambda: defaultdict(list))

        for npc in active_npcs:
            result[npc.position][npc.organization].append(npc)

        return {pos: dict(orgs) for pos, orgs in result.items()}

    def schedule_actions(self):
        """
        Schedule NPC actions.
        """
        for position, org_with_characters in self.get_active_characters().items():
            logging.debug(f"Scheduling actions for NPCs in position {position} with organization {org_with_characters}")
            context = PositionCharactersBehaviorStateService(position, org_with_characters).prepare()
            for org_name, characters in org_with_characters.items():
                for character in characters:
                    if not character.npc:
                        continue
                    svc = DefaultBehaviorPattern(context.get_context(character), self.factory.actions_acceptor)
                    if svc.can_behave():
                        svc.behave()
