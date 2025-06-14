import random
import typing as t
import uuid

from apps.core.models import DimensionAnomalyEffect, CharacterStats, ItemType, DimensionAnomalyInteractionResult, \
    ActionImpactModel, ImpactType, ImpactViolationType
from apps.game.services.character.character_items import CharacterItemsService
from apps.game.services.rand_dice import DiceService
from apps.items.models import Item, WorldItem

if t.TYPE_CHECKING:
    from apps.core.models import DimensionAnomaly
    from apps.game.services.character.core import CharacterService


class AnomalyDetector:
    def __init__(self, anomaly: "DimensionAnomaly"):
        self.anomaly = anomaly
        self.__result__ = DimensionAnomalyInteractionResult(
            gained_impacts=[],
            gained_items=[],
            dice_roll_result=None
        )

    def _register_impact(self, impact: ActionImpactModel):
        self.__result__.gained_impacts.append(impact)

    def _obtain_item(self, item_id: uuid.UUID):
        self.__result__.gained_items.append(item_id)

    def detect(self, character: "CharacterService") -> DimensionAnomalyInteractionResult:

        dice_svc = DiceService(character.character, luck=character.get_stat(CharacterStats.LUCK), sides=20)
        items_svc = CharacterItemsService(character.character)
        self.__result__.dice_roll_result = dice_svc.multiplier_roll()
        result = self.__result__.dice_roll_result.dice_side

        if self.anomaly.effect == DimensionAnomalyEffect.Negative:
            if result == 1:
                # Kill player by removing all health points, action points, and flow points
                character.knock_out()
                # Register KNOCK_OUT impact
                impact = ActionImpactModel(
                    type=ImpactType.KNOCK_OUT,
                    violation=ImpactViolationType.PHYSICAL,
                    size=100,
                    dice_roll_result=self.__result__.dice_roll_result
                )
                self._register_impact(impact)
            elif 2 <= result <= 4:
                # Decrease action points and flow points drastically and remove health points majorly
                ap_amount = character.get_current_ap()
                energy_amount = int(character.get_current_energy() * 0.8)
                hp_amount = int(character.get_current_hp() * 0.7)

                character.spend_ap(ap_amount)  # Remove all action points
                character.spend_energy(energy_amount)  # Remove 80% of energy points
                character.spend_hp(hp_amount)  # Remove 70% of health points

                # Register impacts
                self._register_impact(ActionImpactModel(
                    type=ImpactType.DAMAGE,
                    violation=ImpactViolationType.PHYSICAL,
                    size=hp_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.ENERGY_DECREASE,
                    violation=ImpactViolationType.ENERGY,
                    size=energy_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.ENERGY_DECREASE,
                    violation=ImpactViolationType.ENERGY,
                    size=ap_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
            elif 5 <= result <= 9:
                # Decrease action points and flow points drastically and remove health points moderately
                ap_amount = int(character.get_current_ap() * 0.8)
                energy_amount = int(character.get_current_energy() * 0.7)
                hp_amount = int(character.get_current_hp() * 0.5)

                character.spend_ap(ap_amount)  # Remove 80% of action points
                character.spend_energy(energy_amount)  # Remove 70% of energy points
                character.spend_hp(hp_amount)  # Remove 50% of health points

                # Register impacts
                self._register_impact(ActionImpactModel(
                    type=ImpactType.DAMAGE,
                    violation=ImpactViolationType.PHYSICAL,
                    size=hp_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.ENERGY_DECREASE,
                    violation=ImpactViolationType.ENERGY,
                    size=energy_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.ENERGY_DECREASE,
                    violation=ImpactViolationType.ENERGY,
                    size=ap_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
            elif 10 <= result <= 14:
                # Decrease action points and flow points moderately and remove health points minorly
                ap_amount = int(character.get_current_ap() * 0.5)
                energy_amount = int(character.get_current_energy() * 0.5)
                hp_amount = int(character.get_current_hp() * 0.3)

                character.spend_ap(ap_amount)  # Remove 50% of action points
                character.spend_energy(energy_amount)  # Remove 50% of energy points
                character.spend_hp(hp_amount)  # Remove 30% of health points

                # Register impacts
                self._register_impact(ActionImpactModel(
                    type=ImpactType.DAMAGE,
                    violation=ImpactViolationType.PHYSICAL,
                    size=hp_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.ENERGY_DECREASE,
                    violation=ImpactViolationType.ENERGY,
                    size=energy_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.ENERGY_DECREASE,
                    violation=ImpactViolationType.ENERGY,
                    size=ap_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
            elif 15 <= result <= 17:
                # Decrease action points and flow points drastically
                ap_amount = int(character.get_current_ap() * 0.7)
                energy_amount = int(character.get_current_energy() * 0.7)

                character.spend_ap(ap_amount)  # Remove 70% of action points
                character.spend_energy(energy_amount)  # Remove 70% of energy points

                # Register impacts
                self._register_impact(ActionImpactModel(
                    type=ImpactType.ENERGY_DECREASE,
                    violation=ImpactViolationType.ENERGY,
                    size=energy_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.ENERGY_DECREASE,
                    violation=ImpactViolationType.ENERGY,
                    size=ap_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
            elif 18 <= result <= 20:
                # Just decrease action points
                ap_amount = int(character.get_current_ap() * 0.5)
                character.spend_ap(ap_amount)  # Remove 50% of action points

                # Register impact
                self._register_impact(ActionImpactModel(
                    type=ImpactType.ENERGY_DECREASE,
                    violation=ImpactViolationType.ENERGY,
                    size=ap_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))

        elif self.anomaly.effect == DimensionAnomalyEffect.Positive:
            if 1 <= result <= 4:
                # Increase flow points and action points moderately
                energy_amount = int(character.get_max_energy() * 0.5)
                ap_amount = int(character.get_max_ap() * 0.5)

                character.add_energy(energy_amount)  # Add 50% of max energy points
                character.add_ap(ap_amount)  # Add 50% of max action points

                # Register impacts
                self._register_impact(ActionImpactModel(
                    type=ImpactType.REGENERATION,
                    violation=ImpactViolationType.ENERGY,
                    size=energy_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.HASTE,
                    violation=ImpactViolationType.NONE,
                    size=ap_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
            elif 5 <= result <= 9:
                # Fulfill flow points and action points
                energy_amount = character.get_max_energy()
                ap_amount = character.get_max_ap()

                character.add_energy(energy_amount)  # Fill energy points to max
                character.add_ap(ap_amount)  # Fill action points to max

                # Register impacts
                self._register_impact(ActionImpactModel(
                    type=ImpactType.REGENERATION,
                    violation=ImpactViolationType.ENERGY,
                    size=energy_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.HASTE,
                    violation=ImpactViolationType.NONE,
                    size=ap_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
            elif 10 <= result <= 14:
                # Heal health points minorly and fulfill flow points and action points
                hp_amount = int(character.get_max_hp() * 0.3)
                energy_amount = character.get_max_energy()
                ap_amount = character.get_max_ap()

                character.add_hp(hp_amount)  # Add 30% of max health points
                character.add_energy(energy_amount)  # Fill energy points to max
                character.add_ap(ap_amount)  # Fill action points to max

                # Register impacts
                self._register_impact(ActionImpactModel(
                    type=ImpactType.HEAL,
                    violation=ImpactViolationType.NONE,
                    size=hp_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.REGENERATION,
                    violation=ImpactViolationType.ENERGY,
                    size=energy_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.HASTE,
                    violation=ImpactViolationType.NONE,
                    size=ap_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
            elif 15 <= result <= 17:
                # Full heal health points and fulfill flow points and action points
                hp_amount = character.get_max_hp()
                energy_amount = character.get_max_energy()
                ap_amount = character.get_max_ap()

                character.add_hp(hp_amount)  # Fill health points to max
                character.add_energy(energy_amount)  # Fill energy points to max
                character.add_ap(ap_amount)  # Fill action points to max

                # Register impacts
                self._register_impact(ActionImpactModel(
                    type=ImpactType.HEAL,
                    violation=ImpactViolationType.NONE,
                    size=hp_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.REGENERATION,
                    violation=ImpactViolationType.ENERGY,
                    size=energy_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.HASTE,
                    violation=ImpactViolationType.NONE,
                    size=ap_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
            elif 18 <= result <= 20:
                # Give player with random item of type: `food` or `artifact`
                item_type = random.choice([ItemType.FOOD, ItemType.ARTIFACT])
                # Get a random item of the selected type
                random_item = Item.objects.filter(type=item_type).order_by('?').first()
                if random_item:
                    # Create a WorldItem from the Item
                    world_item = WorldItem.objects.create(
                        item=random_item,
                        position=character.character.position
                    )
                    # Add the item to the character's inventory using CharacterItemsService
                    items_svc.pick_item(world_item)
                    # Register obtained item
                    self._obtain_item(world_item.id)

                # Also fulfill flow points and action points
                energy_amount = character.get_max_energy()
                ap_amount = character.get_max_ap()

                character.add_energy(energy_amount)  # Fill energy points to max
                character.add_ap(ap_amount)  # Fill action points to max

                # Register impacts
                self._register_impact(ActionImpactModel(
                    type=ImpactType.REGENERATION,
                    violation=ImpactViolationType.ENERGY,
                    size=energy_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))
                self._register_impact(ActionImpactModel(
                    type=ImpactType.HASTE,
                    violation=ImpactViolationType.NONE,
                    size=ap_amount,
                    dice_roll_result=self.__result__.dice_roll_result
                ))

        # Mark the anomaly as known
        self.anomaly.known = True
        self.anomaly.save()

        return self.__result__
