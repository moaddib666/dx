import typing
from functools import partial

from django.db.models import QuerySet, Q, F

from apps.action.models import Cycle
from apps.character.models import Character
from apps.core.models import EffectType
from apps.shields.models import ActiveShield
from apps.world.models import SubLocation
from .accept import ActionAcceptor
from .base_service import CharacterActionPlayerServicePrototype, ActionResultNotifier
from .npc_action_scheduler import NpcActionScheduler
from .stat_changes_applyer import BaseStatChangesApplier
from ..character.core import CharacterService
from ..npc.bahavior_factory import BehaviorFactory
from ..shield import ActiveShieldLifeCycleService

if typing.TYPE_CHECKING:
    from .factory import CharacterActionFactory
    from ..effect.facctory import ApplyEffectFactory, ManagerEffectFactory
    from ..world.auto_map import AutoMapService


class ManualCharacterActionPlayerService(CharacterActionPlayerServicePrototype):
    char_svc_cls = CharacterService
    active_shields_cls = ActiveShieldLifeCycleService

    def __init__(self, cycle: Cycle, factory: "CharacterActionFactory", notify_svc: "ActionResultNotifier",
                 effects_apply_factory: "ApplyEffectFactory",
                 effects_manager_factory: "ManagerEffectFactory",
                 auto_map_svc: "AutoMapService",
                 ):
        self.cycle = cycle
        self.factory = factory
        self.notify_svc = notify_svc
        self.effects_apply_factory = effects_apply_factory
        self.effects_manager_factory = effects_manager_factory
        self.base_stats_applier = BaseStatChangesApplier()
        self.npc_actions_scheduler = NpcActionScheduler(
            BehaviorFactory(
                actions_acceptor=partial(ActionAcceptor, factory=factory)
            )
        )
        self.auto_map_svc = auto_map_svc

    def prepare(self):
        self.base_stats_applier.apply()
        self.npc_actions_scheduler.schedule_actions()
        self.auto_map_svc.map_characters()

    def post(self):
        self.update_characters()
        self.active_shields_cls(self.get_active_shields()).decrease_cycles()

    def play(self) -> Cycle:
        self._play()
        self.post()
        next_cycle = Cycle.objects.next()
        self.prepare()
        return next_cycle

    def _play(self):
        self.apply_effects()
        self.apply_actions()

    def apply_actions(self):
        for action in self.get_actions():
            self.apply_single_action(action)

    def apply_single_action(self, action):
        try:
            action_service = self.factory.from_action(action)
            action_service.check(action)  # FIXME: it looks like the dead chars perform actions after death
            action_service.perform(action)
            action.perform()
            self.notify_svc.notify(action)
        except Exception as e:
            self.notify_svc.notify(action, e)

    def apply_effects(self):
        qs = Character.objects.filter(is_active=True)
        for char in qs:
            for effect in char.effects.all():
                svc = self.effects_apply_factory.from_active_effect(effect)
                svc.apply_effect(char)

    def update_characters(self):
        for char in self._get_suitable_characters():

            if not char.model.npc:
                print(char.model)
            self.remove_inactive_effects(char)
            if char.is_knocked_out():
                if not char.has_effects([EffectType.KNOCKED_OUT, EffectType.COMA]):
                    manager = self.effects_manager_factory.from_effect_id(EffectType.KNOCKED_OUT)
                    manager.remove_all_effects(char)
                    manager.assign_world_effect(EffectType.KNOCKED_OUT, char)
                continue
            if char.has_effects([EffectType.KNOCKED_OUT]):
                manager = self.effects_manager_factory.from_effect_id(EffectType.COMA)
                manager.remove_effect(EffectType.KNOCKED_OUT, char)

            char.refill_ap()

    def remove_inactive_effects(self, char: CharacterService):
        expired_e = char.model.effects.filter(
            Q(effect__permanent=False) & Q(duration__gte=0) & Q(duration__gte=F("ends_in"))
        ).select_related("effect")
        self.effects_manager_factory.default().remove_many([
            effect.effect.id for effect in expired_e
        ], char)

    def _active_sub_loactions(self) -> [SubLocation]:
        """
        Retrutn sub locaton where at least one non npc character is active
        """
        return Character.objects.filter(is_active=True, npc=False).values_list("position__sub_location",
                                                                               flat=True).distinct()

    def _get_suitable_characters(self) -> ["CharacterService"]:
        """
        take characters that have hp > 0 and not stunned
        :return:
        """
        # Lets make performance better and fiend only
        # 1. active non-npc characters
        # 2. active npc characters that has characters in current or current + 3 positions

        filtered = (
                Character.objects.filter(is_active=True, npc=False) |
                Character.objects.filter(is_active=True, npc=True, position__sub_location__in=self._active_sub_loactions())
        )

        return (self.char_svc_cls(char) for char in filtered)

    def get_actions(self) -> QuerySet:
        return self.cycle.actions.filter(performed=False, accepted=True).order_by(
            "order"
        ).select_related("initiator", "skill", "item", "position")

    def get_active_shields(self) -> QuerySet:
        return ActiveShield.objects.all()
