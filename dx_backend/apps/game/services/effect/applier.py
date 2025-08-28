import abc
from abc import ABC

from apps.character.models import Character
from apps.core.models import EffectType
from apps.effects.models import ActiveEffect
from apps.game.services.character.core import CharacterService
from apps.world.models import Position
from .assigner import DefaultEffectManager


class BaseActiveEffectService(abc.ABC):
    @abc.abstractmethod
    def is_applicable(self, target: 'Character') -> bool:
        pass

    @abc.abstractmethod
    def apply(self, target: 'Character') -> None:
        pass

    def apply_effect(self, target: 'Character') -> None:
        if not self.is_applicable(target):
            return
        self._update_counters()
        if self._is_first_application():
            self.on_start(target)
        self.apply(target)
        if self._is_last_application():
            self.on_finish(target)

    def on_start(self, target: 'Character') -> None:
        pass

    def on_finish(self, target: 'Character') -> None:
        pass

    def _is_first_application(self) -> bool:
        return False

    def _is_last_application(self) -> bool:
        return False

    def _update_counters(self) -> None:
        pass


class DefaultActiveEffectService(BaseActiveEffectService, ABC):
    char_svc = CharacterService
    effect_assign_svc = DefaultEffectManager

    def __init__(self, active_effect: ActiveEffect):
        self.active_effect = active_effect

    def is_applicable(self, target: 'Character') -> bool:
        char_svc = CharacterService(target)
        return not char_svc.is_knocked_out()

    def _update_counters(self) -> None:
        self.active_effect.duration += 1
        # if self._is_last_application():
        #     self.active_effect.active = False
        self.active_effect.save(update_fields=['duration', 'active', 'updated_at'])

    def _is_first_application(self) -> bool:
        return self.active_effect.duration == 1

    def _is_last_application(self) -> bool:
        if self.active_effect.effect.permanent:
            return False
        if self.active_effect.ends_in:
            return self.active_effect.duration >= self.active_effect.ends_in
        return self.active_effect.duration >= self.active_effect.effect.ends_in


class UnknownActiveEffectService(DefaultActiveEffectService):

    def is_applicable(self, target: 'Character') -> bool:
        return True

    def apply(self, target: 'Character') -> None:
        pass


class KnockOutActiveEffectService(DefaultActiveEffectService):

    def apply(self, target: 'Character') -> None:
        pass

    def is_applicable(self, target: 'Character') -> bool:
        char_svc = self.char_svc(target)
        return not char_svc.has_effects(EffectType.COMA) and char_svc.is_knocked_out()

    def on_start(self, target: 'Character') -> None:
        super().on_start(target)
        char_svc = self.char_svc(target)
        char_svc.knock_out()

    def on_finish(self, target: 'Character') -> None:
        super().on_finish(target)
        self.effect_assign_svc().assign_world_effect(EffectType.COMA, self.char_svc(target))


class KomaActiveEffectService(DefaultActiveEffectService):

    def is_applicable(self, target: 'Character') -> bool:
        char_svc = self.char_svc(target)
        return char_svc.has_effect(EffectType.COMA) and char_svc.is_knocked_out()

    def apply(self, target: 'Character') -> None:
        pass

    def on_start(self, target: 'Character') -> None:
        super().on_start(target)
        char_svc = self.char_svc(target)
        char_svc.knock_out()

    def on_finish(self, target: 'Character') -> None:
        super().on_finish(target)
        char_svc = self.char_svc(target)
        # Teleport to the safe place
        # Add 1 hp and 1 energy
        char_svc.add_hp(1)
        char_svc.add_energy(50)

        # TODO: use position service to teleport to the safe place
        if char_svc.model.npc:
            # check if npc been spawned by spawner
            if hasattr(char_svc.model, 'spawned_by'):
                char_svc.model.delete()
                return
            char_svc.model.is_active = False
            char_svc.model.save(update_fields=['is_active', 'updated_at'])
            return

        char_svc.character.position = char_svc.character.last_safe_position or Position.objects.get(grid_x=0, grid_y=1, grid_z=1)
        char_svc.character.save(update_fields=['position', 'updated_at'])


