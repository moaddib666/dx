import abc

from apps.character.models import Character
from apps.core.models import EffectType
from apps.effects.models import Effect


class BaseEffectAssigner(abc.ABC):

    def assign_effect(self, effect_id: EffectType, target: Character, initiator: Character = None):
        self.assign(effect_id, target, initiator)

    def remove_effect(self, effect_id: EffectType, target: Character, initiator: Character = None):
        self.remove(effect_id, target, initiator)

    def remove_all_effects(self, target: Character, initiator: Character = None):
        self.remove_all(target, initiator)

    def assign_many_effects(self, effect_ids: list[EffectType], target: Character, initiator: Character = None):
        self.assign_many(effect_ids, target, initiator)

    @abc.abstractmethod
    def assign(self, effect_id: EffectType, target: Character, initiator: Character = None):
        pass

    @abc.abstractmethod
    def remove(self, effect_id: EffectType, target: Character, initiator: Character = None):
        pass

    @abc.abstractmethod
    def remove_all(self, target: Character, initiator: Character = None):
        pass

    @abc.abstractmethod
    def assign_many(self, effect_ids: list[EffectType], target: Character, initiator: Character = None):
        pass


class DefaultEffectManager(BaseEffectAssigner):
    model = Effect

    def assign(self, effect_id: EffectType, target: Character, initiator: Character = None):
        effect, _ = self.model.objects.get_or_create(id=effect_id,
                                                     defaults={'icon': None, 'permanent': False, 'ends_in': 1})
        # TODO: add construct the impact
        target.effects.update_or_create(effect=effect, defaults={'duration': 0, 'impact': {}})

    def remove(self, effect_id: EffectType, target: Character, initiator: Character = None):
        target.effects.filter(effect_id=effect_id).update(active=False)

    def remove_all(self, target: Character, initiator: Character = None):
        target.effects.update(active=False)

    def assign_many(self, effect_ids: list[EffectType], target: Character, initiator: Character = None):
        for effect_id in effect_ids:
            self.assign(effect_id, target)
