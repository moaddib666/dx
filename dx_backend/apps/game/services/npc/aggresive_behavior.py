import functools
import typing as t

from django.db.models import Q

from apps.action.models import CharacterAction, Cycle
from apps.character.models import Character
from apps.core.models import CharacterStats, SkillTypes, AttributeType
from apps.game.services.character.core import CharacterService
from .base_behavior import BaseBehaviorService


class AggressiveBehaviorService(BaseBehaviorService):
    """
    Aggressive behavior service.
    """

    def __init__(self, character, action_acceptor) -> None:
        super().__init__(character, action_acceptor)
        self.visible_targets = []
        self.character_svc = CharacterService(character)

        self._scheduled_heal = False
        self._scheduled_shield = False
        self._scheduled_energy = False

    @functools.cache
    def get_potential_enemies(self) -> [Character]:
        return Character.objects.filter(
            position=self.character.position,
        ).exclude(
            organization=self.character.organization,
        )

    @functools.cache
    def get_potential_friends(self) -> [Character]:
        return Character.objects.filter(
            is_active=True,
            position=self.character.position,
            organization=self.character.organization,
        )

    def is_target_visible(self, target: Character) -> bool:
        """
        Check if the target is visible to the NPC.
        """
        current_cycle = Cycle.objects.current()
        actions_made_by_targets_aimed_at_npc = CharacterAction.objects.filter(
            initiator__in=self.get_potential_enemies(),
            targets__in=(self.get_potential_friends() | Character.objects.filter(id=self.character.id)).all(),
            # position=self.character.position, # FIXME: fix this in acceptance service
            cycle_id__gte=current_cycle.id - 5,
        )
        if actions_made_by_targets_aimed_at_npc.exists():
            self.logger.debug(
                f"Actions made by potential friends aimed at NPC: {actions_made_by_targets_aimed_at_npc.count()}"
            )
            return True

        action_made_by_npc_aimed_at_target = CharacterAction.objects.filter(
            initiator__in=(self.get_potential_friends() | Character.objects.filter(id=self.character.id)).all(),
            targets__in=self.get_potential_enemies(),
            # position=self.character.position,
            cycle_id__gte=current_cycle.id - 5,
        )

        if action_made_by_npc_aimed_at_target.exists():
            self.logger.debug(
                f"Actions made by potential friends aimed at player: {action_made_by_npc_aimed_at_target.count()}"
            )
            return True

        target_char = CharacterService(target)
        target_speed = target_char.get_stat(CharacterStats.SPEED)
        target_luck = target_char.get_stat(CharacterStats.LUCK)

        npc_speed = self.character_svc.get_stat(CharacterStats.SPEED)
        npc_luck = self.character_svc.get_stat(CharacterStats.LUCK)

        npc_dice = self.character_svc.get_dice_service()(sides=20)
        target_dice = target_char.get_dice_service()(sides=20)

        npc_roll = npc_dice.roll() + npc_speed + npc_luck
        char_roll = target_dice.roll() + target_speed + target_luck
        self.logger.debug(f"NPC roll: {npc_roll}, Char roll: {char_roll}")
        if npc_roll > char_roll:
            self.logger.debug(f"NPC won the roll against {target}")
            return True
        self.logger.debug(f"NPC lost the roll against {target}")

    def scan_targets(self) -> [Character]:
        """"
        Find Non NPC Characters in this position.
        Check if they are in the NPC's range of sight in same organization or not.
        Check if they are ane action been done by Player on NPC from the same organization in this position.
        If still not - Drop The dice d20 and player drops d20. add luck and speed to the result.
        If NPC wins - add player to the visible_targets.
        """
        return [
            target for target in self.get_potential_enemies() if self.is_target_visible(target)
        ]

    def behave(self):
        self.visible_targets = self.scan_targets()
        super().behave()

    def make_default_action(self) -> t.Optional[CharacterAction]:
        # Make attack action here
        if not self.has_targets():
            return None
        learned_skill = self.character.learned_skills.filter(
            skill__type=SkillTypes.ATTACK,
        ).select_related('skill').order_by('skill__grade', 'is_base')
        if not learned_skill:
            return None
        # select most suitable by action points
        for skill in learned_skill:
            for cost in skill.skill.cost:
                if cost["kind"] == AttributeType.ACTION_POINTS:
                    if cost["value"] <= self.character_svc.get_current_ap():
                        return self.make_skill_action(skill.skill, self.visible_targets)

    def has_targets(self) -> bool:
        return bool(self.visible_targets)
