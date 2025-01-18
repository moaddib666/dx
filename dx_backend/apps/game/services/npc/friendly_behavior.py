import functools
import typing as t

from apps.action.models import CharacterAction
from apps.character.models import Character
from apps.game.services.npc.base_behavior import BaseBehaviorService


class FriendlyBehaviorService(BaseBehaviorService):
    """
    Friendly behavior service for NPCs.
    Focuses on healing, shielding, and buffing allies.
    """

    def __init__(self, character: Character, action_acceptor) -> None:
        super().__init__(character, action_acceptor)
        self._scheduled_heal = False
        self._scheduled_buff = False

    @functools.cache
    def get_potential_allies(self) -> [Character]:
        """
        Retrieve allies in the same position and organization as the NPC.
        Excludes the NPC itself.
        """
        return (Character.objects.filter(
            position=self.character.position,
            organization=self.character.organization,
        ).exclude(id=self.character.id) | Character.objects.filter(
            position=self.character.position,
            npc=False,
        )).distinct().all()


    def make_default_action(self) -> t.Optional[CharacterAction]:
        """
        Override the default action to prioritize supporting allies.
        """

        if self.has_heal_skill() and self._scheduled_heal is False:
            self._scheduled_heal = True
            return self.make_heal_action(self.get_potential_allies())

        # FIXME: buf is not supported yet
        # if self.has_buff_skill() and self._scheduled_buff is False:
        #     self._scheduled_buff = True
        #     return self.make_buff_action(self.get_potential_allies())

        # Shielding allies is a lower priority byt default
        if self.has_shield_skill():
            # Prioritize shielding allies
            return self.make_shield_action(self.get_potential_allies())

        return None
