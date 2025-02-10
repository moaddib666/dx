import abc
import logging
import random
import typing as t

from apps.effects.models import Effect
from apps.game.services.formula.base import FormulaService

if t.TYPE_CHECKING:
    from apps.core.models import EffectType
    from apps.school.dto import AssignableEffect
    from apps.game.services.character.core import CharacterService


class BaseEffectAssigner(abc.ABC):
    formula_svc_cls = FormulaService
    logger = logging.getLogger("services.effect.assigner")

    def assign_world_effect(self, effect_id: "EffectType", target: "CharacterService"):
        core_effect = Effect.objects.get(id=effect_id)
        new_effect, _ = target.model.effects.update_or_create(
            effect=core_effect,
            defaults={
                'impact': {},
                'ends_in': core_effect.ends_in
            }
        )
        self.logger.info(f"Effect {effect_id} applied to {target} with duration {core_effect.ends_in}")

    def assign_effect(self, effect: "AssignableEffect", target: "CharacterService", initiator: "CharacterService"):
        self.assign(effect, target, initiator)

    def remove_effect(self, effect_id: "EffectType", target: "CharacterService",
                      initiator: "CharacterService" = None):
        self.remove(effect_id, target, initiator)

    def remove_all_effects(self, target: "CharacterService", initiator: "CharacterService" = None):
        self.remove_all(target, initiator)

    def assign_many_effects(self, effect_ids: list["EffectType"], target: "CharacterService",
                            initiator: "CharacterService"):
        self.assign_many(effect_ids, target, initiator)

    @abc.abstractmethod
    def assign(self, effect: "AssignableEffect", target: "CharacterService", initiator: "CharacterService"):
        pass

    @abc.abstractmethod
    def remove(self, effect_id: "EffectType", target: "CharacterService", initiator: "CharacterService" = None):
        pass

    @abc.abstractmethod
    def remove_all(self, target: "CharacterService", initiator: "CharacterService" = None):
        pass

    @abc.abstractmethod
    def assign_many(self, effects: list["AssignableEffect"], target: "CharacterService",
                    initiator: "CharacterService"):
        pass


class DefaultEffectManager(BaseEffectAssigner):
    model = Effect

    def assign(self, effect: "AssignableEffect", target: "CharacterService", initiator: "CharacterService"):
        base_chance = effect["base_chance"] * 100
        dice_svc = target.get_dice_service()(
            sides=100,
        )
        rand_result = dice_svc.roll()
        if rand_result < 100 - base_chance:
            self.logger.info(
                f"Effect {effect['name']} failed to apply to {target} with chance {base_chance} and result {rand_result}")
            return
        core_effect, _ = self.model.objects.get_or_create(
            id=effect["name"],
            defaults={
                'icon': None,
                'permanent': False,
                'ends_in': 1,
            }
        )

        duration = self.formula_svc_cls(
            initiator,
            effect["duration_modifier"]["formula"],
            use_real_stats=True
        ).evaluate_int()

        new_effect, _ = target.model.effects.update_or_create(
            effect=core_effect,
            defaults={
                'ends_in': duration,
                'impact': effect.get("impact", {}),
                'duration': 0,
            }
        )
        self.logger.info(f"Effect {effect['name']} applied to {target} with duration {duration}")
        for stat_mod in effect.get("stat_modifiers", []):
            label = stat_mod["label"]
            value = self.formula_svc_cls(
                initiator,
                stat_mod["formula"],
                use_real_stats=True,
            ).evaluate_int()
            self.logger.info(f"Applying stat modifier {label} with value {value} to {target}")
            # FIXME: enshure dedublication
            new_effect.applied_stat_modifiers.update_or_create(
                name=label,
                character=target.model,
                defaults={
                    'value': value
                }
            )

    def remove(self, effect_id: "EffectType", target: "CharacterService", initiator: "CharacterService" = None):
        self.remove_inactive_modifiers(target)
        target.model.effects.filter(effect_id=effect_id).delete()
        self.logger.info(f"Effect {effect_id} removed from {target}")

    def remove_inactive_modifiers(self, target: "CharacterService"):
        target.model.stats_modifiers.filter(applied_by_effect__active=False).delete()
        self.logger.info(f"Removed inactive stat modifiers from {target}")

    def remove_all(self, target: "CharacterService", initiator: "CharacterService" = None):
        count = target.model.effects.update(active=False)
        if not count:
            return
        self.logger.info(f"All effects removed from {target}")
        self.remove_inactive_modifiers(target)

    def assign_many(self, effects: list["AssignableEffect"], target: "CharacterService",
                    initiator: "CharacterService"):
        for effect in effects:
            self.assign(effect, target, initiator)

    def remove_many(self, effects: list["EffectType"], target: "CharacterService"):
        count = target.model.effects.filter(effect_id__in=effects).update(active=False)
        if not count:
            return
        self.logger.info(f"Effects {effects} removed from {target}")
        self.remove_inactive_modifiers(target)
