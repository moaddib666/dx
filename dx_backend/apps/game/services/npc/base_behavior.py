import random
import random
import typing as t

from apps.action.models import CharacterAction, Cycle
from apps.character.models import Character
from apps.core.models import SkillTypes, GameObject
from apps.game.services.character.core import CharacterService
from apps.game.services.npc.behavior import BehaviorServiceProtocol
from apps.school.models import Skill


class BaseBehaviorService(BehaviorServiceProtocol):
    """
    Base behavior service.
    """

    def __init__(self, character, action_acceptor) -> None:
        super().__init__(character, action_acceptor)
        self.character_svc = CharacterService(character)

        self._scheduled_heal = False
        self._scheduled_shield = False
        self._scheduled_energy = False

    def behave(self) -> None:
        last_ap = self.character_svc.get_current_ap()
        while self.can_behave():
            action = None
            if self.need_energy() and self.has_energy_skill():
                action = self.make_self_energy_action()
            elif self.need_shield() and self.has_shield_skill():
                action = self.make_self_shield_action()
            elif self.need_heal() and self.has_heal_skill():
                action = self.make_self_heal_action()
            else:
                action = self.make_default_action()
                if not action:
                    break
            if not action:
                continue
            try:
                self.logger.debug(f"Scheduling action for {self.character}: {action}")
                self.accept_action(action)
            except Exception as e:
                self.logger.debug(f"Error while making default action: {e}")
                break
            if last_ap == self.character_svc.get_current_ap():
                break
            last_ap = self.character_svc.get_current_ap()

    def make_self_energy_action(self) -> t.Optional[CharacterAction]:
        return self.make_energy_action([self.character])

    def make_self_shield_action(self) -> t.Optional[CharacterAction]:
        return self.make_shield_action([self.character])

    def make_self_heal_action(self) -> t.Optional[CharacterAction]:
        return self.make_heal_action([self.character])

    def make_skill_action(self, skill: Skill, targets: [GameObject]) -> CharacterAction:
        action = CharacterAction.objects.create(
            action_type=CharacterAction.ActionType.USE_SKILL,
            initiator=self.character,
            skill=skill,
            position=self.character.position,
            cycle=Cycle.objects.current(),
        )
        # FIXME: make skill multi-target support
        # we need to select target randomly
        target = random.choice(targets)
        action.targets.add(target)
        return action

    def has_heal_skill(self) -> bool:
        return self.character.learned_skills.filter(
            skill__type=SkillTypes.HEAL,
        ).exists()

    def has_shield_skill(self) -> bool:
        return self.character.learned_skills.filter(
            skill__type=SkillTypes.DEFENSE,
        ).exists()

    def has_energy_skill(self) -> bool:
        return Skill.objects.filter(
            name="Flow Accumulation").exists()

    def make_heal_action(self, targets: [Character]) -> t.Optional[CharacterAction]:
        self._scheduled_heal = True
        # Make heal action here
        learned_skill = self.character.learned_skills.select_related('skill').filter(
            skill__type=SkillTypes.HEAL,
        ).order_by('skill__grade', "is_base").first()
        if not learned_skill:
            return None
        target = random.choice(targets)
        return self.make_skill_action(learned_skill.skill, [target])

    def make_shield_action(self, targets: [Character]) -> t.Optional[CharacterAction]:
        self._scheduled_shield = True
        # Make shield action here
        learned_skill = self.character.learned_skills.filter(
            skill__type=SkillTypes.DEFENSE,
        ).select_related('skill').order_by('skill__grade', "is_base").first()
        if not learned_skill:
            return None
        target = random.choice(targets)
        return self.make_skill_action(learned_skill.skill, [target])

    def make_energy_action(self, targets: [Character]) -> t.Optional[CharacterAction]:
        self._scheduled_energy = True
        # Make energy action here
        learned_skill = Skill.objects.filter(
            name="Flow Accumulation").first()
        if not learned_skill:
            return None
        target = random.choice(targets)
        return self.make_skill_action(learned_skill, [target])

    def make_default_action(self) -> t.Optional[CharacterAction]:
        pass

    def make_buff_action(self, targets: [Character]) -> t.Optional[CharacterAction]:
        """
        Create a buff action targeting the specified ally.
        """
        learned_skill = self.character.learned_skills.filter(
            skill__type=SkillTypes.BUFF,
        ).select_related('skill').order_by('skill__grade').first()
        if not learned_skill:
            return None
        target = random.choice(targets)
        return self.make_skill_action(learned_skill.skill, [target])

    def make_self_buff_action(self) -> t.Optional[CharacterAction]:
        """
        Create a buff action targeting the NPC itself.
        """
        return self.make_buff_action([self.character])

    def has_buff_skill(self) -> bool:
        """
        Check if the NPC has any buff skills.
        """
        return self.character.learned_skills.filter(
            skill__type=SkillTypes.BUFF,
        ).exists()

    def has_targets(self) -> bool:
        return False

    def need_energy(self) -> bool:
        """
        if energy < 30% of max energy
        refill energy need to be done.
        """
        return self.character_svc.get_current_energy() < 0.3 * self.character_svc.get_max_energy() and not self._scheduled_energy

    def need_shield(self) -> bool:
        """
        if no shields - need shielding
        if shields are  <= 2 grade - need shielding
        """
        have_active_shields = self.character_svc.get_shields()
        if not have_active_shields:
            return True and not self._scheduled_shield
        for shield in have_active_shields:
            if shield.level <= 2:
                return True and not self._scheduled_shield
        return False

    def need_heal(self) -> bool:
        """
        if health < 65% of max health heal need to be done.
        """
        return self.character_svc.get_current_hp() < 0.65 * self.character_svc.get_max_hp() and not self._scheduled_heal

    def can_behave(self) -> bool:
        """
        If have action points and not stuck by some effect etc.
        """
        return self.character_svc.get_current_ap() > 0 and not self.character_svc.is_knocked_out()
