from apps.core.models import EffectType
from apps.effects.models import Effect, ActiveEffect
from .applier import DefaultActiveEffectService, KnockOutActiveEffectService, \
    KomaActiveEffectService, UnknownActiveEffectService
from .assigner import DefaultEffectManager


class ManagerEffectFactory:

    def from_effect(self, effect: Effect) -> DefaultEffectManager:
        return DefaultEffectManager()

    def from_effect_id(self, effect_id: str) -> DefaultEffectManager:
        return DefaultEffectManager()

    def from_action(self, action: 'CharacterAction') -> DefaultEffectManager:
        return DefaultEffectManager()


class ApplyEffectFactory:
    mapping = {
        EffectType.KNOCKED_OUT: KnockOutActiveEffectService,
        EffectType.COMA: KomaActiveEffectService
    }

    def from_active_effect(self, active_effect: 'ActiveEffect') -> DefaultActiveEffectService:
        effect_type = active_effect.effect.id
        return self.mapping.get(effect_type, UnknownActiveEffectService)(active_effect)
