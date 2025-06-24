import logging
import random
import typing as t
from functools import partial

from apps.action.models import CharacterAction, Cycle
from apps.core.models import SkillTypes, CharacterActionType
from apps.game.exceptions import GameException
from apps.game.services.action.npc.target import TargetSelectionStrategy, RandomSelectCompositeStrategy, \
    TwoToOneStrategy, AggressiveStrategy, DefensiveStrategy, ChaosMonkeyStrategy

if t.TYPE_CHECKING:
    from apps.game.services.character.core import CharacterService
    from apps.game.services.action.npc.context import CharacterPositionActionContext
    from apps.game.services.action.accept import ActionAcceptor


class BehaviorPattern(t.Protocol):
    """
    Protocol for behavior services.
    """
    logger = logging.getLogger("game.service.npc.behavior")
    target_selector: "TargetSelectionStrategy"

    def __init__(self, ctx: "CharacterPositionActionContext", action_acceptor: partial["ActionAcceptor"]) -> None:
        self.ctx = ctx
        self.action_acceptor = action_acceptor

    def behave(self):
        ...

    def has_targets(self) -> bool:
        ...

    def can_behave(self) -> bool:
        ...

    def accept_action(self, action: 'CharacterAction') -> bool:
        """
        Accepts an action and schedules it for execution.
        """
        try:
            self.action_acceptor(action).accept()
        except GameException as e:
            self.logger.error(f"Error while accepting action: {e}")
            return False
        return True

    def accept_actions(self, actions: t.Iterable['CharacterAction']) -> bool:
        """
        Accepts multiple actions and schedules them for execution.
        """
        for action in actions:
            if not self.accept_action(action):
                return False
        return True


class DefaultBehaviorPattern(BehaviorPattern):
    """
    Default behavior pattern that does nothing.
    """

    def __init__(self, ctx: "CharacterPositionActionContext", action_acceptor: partial["ActionAcceptor"]) -> None:
        super().__init__(ctx, action_acceptor)
        self.target_selector = RandomSelectCompositeStrategy(ctx, [
            TwoToOneStrategy(ctx),
            AggressiveStrategy(ctx),
            DefensiveStrategy(ctx),
            ChaosMonkeyStrategy(ctx),

        ])

    def behave(self):
        """
        1. Do I need shield? If yes add shield action.
        2. Do i need heal? If yes add heal action.
        3. Do we have enemies ?
        4. Do we have friends ?
        5. What is preferable healing/buffing friends or attacking enemies?
         - If we have enemies near to knockout attack them. <= 30% health
         - If we have friends with low health, heal them. <= 30% health
         - If we can give shield to friends - give shield to friends. need find frineds that does not have shields
        6. Select targets based on strategy for attack or defense.
        7. Return empty list if no actions needed.
        """
        shield_self = StandardShieldBehavior(self.ctx, self.ctx.character, SkillTypes.DEFENSE)
        if shield_self.can_behave():
            self.accept_actions(shield_self.behave())
        heal_self = StandardHealBehavior(self.ctx, self.ctx.character, SkillTypes.HEAL)
        if heal_self.can_behave():
            self.accept_actions(heal_self.behave())

        if not self.has_targets():
            return

        to_attack = self.target_selector.select_attack_targets()
        to_defence = self.target_selector.select_defense_targets()

        deffence_target = random.choice(to_defence) if to_defence else None
        attack_target = random.choice(to_attack) if to_attack else None

        if deffence_target:
            shield_behavior = StandardShieldBehavior(self.ctx, deffence_target, SkillTypes.DEFENSE)
            if shield_behavior.can_behave():
                self.accept_actions(shield_behavior.behave())
            heal_behavior = StandardHealBehavior(self.ctx, deffence_target, SkillTypes.HEAL)
            if heal_behavior.can_behave():
                self.accept_actions(heal_behavior.behave())
        if attack_target:
            attack_behavior = StandardBehavior(self.ctx, attack_target, SkillTypes.ATTACK)
            while attack_behavior.can_behave():
                self.accept_actions(attack_behavior.behave())

    def has_targets(self) -> bool:
        return bool(self.ctx.enemies) or bool(self.ctx.friends)

    def can_behave(self) -> bool:
        return self.ctx.character.get_current_ap() > 0 and not self.ctx.character.is_knocked_out()


class Behavior(t.Protocol):

    def __init__(self, ctx: "CharacterPositionActionContext", target: "CharacterService",
                 skill_type: SkillTypes = SkillTypes.ATTACK) -> None:
        self.ctx = ctx
        self.ability = None
        self.target = target
        self.skill_type = skill_type

    def behave(self, ) -> t.Iterable['CharacterAction']:
        pass

    def can_behave(self) -> bool:
        self.ability = self.ctx.character.can(self.skill_type)
        return self.ability.has_ability()


class StandardBehavior(Behavior):

    def behave(self) -> t.Iterable['CharacterAction']:
        actions = []
        if self.ability.skills:
            # FIXME: uase action factory to create actions
            actions.append(CharacterAction.objects.create(
                initiator=self.ctx.character.character,
                action_type=CharacterActionType.USE_SKILL,
                skill_id=self.ability.skills[0],
                position=self.ctx.character.character.position,
                cycle=Cycle.objects.current(campaign=self.ctx.character.character.campaign),
            ))
        elif self.ability.items:
            actions.append(CharacterAction.objects.create(
                initiator=self.ctx.character.character,
                action_type=CharacterActionType.USE_ITEM,
                item_id=self.ability.items[0],
                position=self.ctx.character.character.position,
                cycle=Cycle.objects.current(campaign=self.ctx.character.character.campaign),
            ))

        for action in actions:
            action.targets.add(self.target.character)
        return actions


class StandardShieldBehavior(StandardBehavior):
    """
    Standard shield behavior that uses the shield skill if available.
    """

    def can_behave(self) -> bool:
        if super().can_behave():
            return not self.target.is_knocked_out() and not self.target.get_shields()
        return False


class StandardHealBehavior(StandardBehavior):
    """
    Standard heal behavior that uses the heal skill if available.
    """

    def can_behave(self) -> bool:
        max_hp = self.target.get_max_hp()
        if max_hp <= 0:
            return False
        health_percentage = self.target.get_current_hp() / max_hp
        if health_percentage > 0.75:
            return False
        return super().can_behave()
