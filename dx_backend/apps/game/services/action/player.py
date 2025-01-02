import typing

from django.db.models import QuerySet

from apps.action.models import Cycle
from apps.character.models import Character
from apps.core.models import EffectType
from .base_service import CharacterActionPlayerServicePrototype, ActionResultNotifier
from ..character.core import CharacterService

if typing.TYPE_CHECKING:
    from .factory import CharacterActionFactory
    from ..effect.facctory import ApplyEffectFactory, ManagerEffectFactory


class ManualCharacterActionPlayerService(CharacterActionPlayerServicePrototype):
    char_svc_cls = CharacterService

    def __init__(self, cycle: Cycle, factory: "CharacterActionFactory", notify_svc: "ActionResultNotifier",
                 effects_apply_factory: "ApplyEffectFactory",
                 effects_manager_factory: "ManagerEffectFactory"
                 ):
        self.cycle = cycle
        self.factory = factory
        self.notify_svc = notify_svc
        self.effects_apply_factory = effects_apply_factory
        self.effects_manager_factory = effects_manager_factory

    def prepare(self):
        pass

    def post(self):
        self.update_characters()

    def play(self):
        self.prepare()
        self._play()
        self.post()

    def _play(self):
        self.apply_effects()
        self.apply_actions()

    def apply_actions(self):
        for action in self.get_actions():
            try:
                action_service = self.factory.from_action(action)
                action_service.check(action)
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
            if char.is_knocked_out():
                if not char.has_effects([EffectType.KNOCKED_OUT, EffectType.COMA]):
                    manager = self.effects_manager_factory.from_effect_id(EffectType)
                    manager.remove_all_effects(char.model)
                    manager.assign_effect(EffectType.KNOCKED_OUT, char.model, initiator=char.model)
                continue
            if char.has_effects([EffectType.KNOCKED_OUT]):
                manager = self.effects_manager_factory.from_effect_id(EffectType.COMA)
                manager.remove_effect(EffectType.KNOCKED_OUT, char.model, initiator=char.model)
            char.refill_ap()

    def _get_suitable_characters(self) -> ["CharacterService"]:
        """
        take characters that have hp > 0 and not stunned
        :return:
        """
        return (self.char_svc_cls(char) for char in Character.objects.filter(is_active=True))

    def get_actions(self) -> QuerySet:
        # TODO: include speed and action size in ordering
        # so that first we execute action that take less action points and the fastest player been first
        return self.cycle.actions.filter(performed=False).order_by("cycle", "created_at")
