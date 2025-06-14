import random
import typing as t

from apps.core.models import DimensionAnomalyEffect, CharacterStats, ItemType
from apps.game.services.character.character_items import CharacterItemsService
from apps.game.services.rand_dice import DiceService
from apps.items.models import Item, WorldItem

if t.TYPE_CHECKING:
    from apps.core.models import DimensionAnomaly
    from apps.game.services.character.core import CharacterService


class AnomalyDetector:
    def __init__(self, anomaly: "DimensionAnomaly"):
        self.anomaly = anomaly

    def detect(self, character: "CharacterService"):

        dice_svc = DiceService(character.character, luck=character.get_stat(CharacterStats.LUCK), sides=20)
        items_svc = CharacterItemsService(character.character)
        result = dice_svc.roll()

        if self.anomaly.effect == DimensionAnomalyEffect.Negative:
            if result == 1:
                # Kill player by removing all health points, action points, and flow points
                character.knock_out()
            elif 2 <= result <= 4:
                # Decrease action points and flow points drastically and remove health points majorly
                character.spend_ap(character.get_current_ap())  # Remove all action points
                character.spend_energy(int(character.get_current_energy() * 0.8))  # Remove 80% of energy points
                character.spend_hp(int(character.get_current_hp() * 0.7))  # Remove 70% of health points
            elif 5 <= result <= 9:
                # Decrease action points and flow points drastically and remove health points moderately
                character.spend_ap(int(character.get_current_ap() * 0.8))  # Remove 80% of action points
                character.spend_energy(int(character.get_current_energy() * 0.7))  # Remove 70% of energy points
                character.spend_hp(int(character.get_current_hp() * 0.5))  # Remove 50% of health points
            elif 10 <= result <= 14:
                # Decrease action points and flow points moderately and remove health points minorly
                character.spend_ap(int(character.get_current_ap() * 0.5))  # Remove 50% of action points
                character.spend_energy(int(character.get_current_energy() * 0.5))  # Remove 50% of energy points
                character.spend_hp(int(character.get_current_hp() * 0.3))  # Remove 30% of health points
            elif 15 <= result <= 17:
                # Decrease action points and flow points drastically
                character.spend_ap(int(character.get_current_ap() * 0.7))  # Remove 70% of action points
                character.spend_energy(int(character.get_current_energy() * 0.7))  # Remove 70% of energy points
            elif 18 <= result <= 20:
                # Just decrease action points
                character.spend_ap(int(character.get_current_ap() * 0.5))  # Remove 50% of action points

        elif self.anomaly.effect == DimensionAnomalyEffect.Positive:
            if 1 <= result <= 4:
                # Increase flow points and action points moderately
                character.add_energy(int(character.get_max_energy() * 0.5))  # Add 50% of max energy points
                character.add_ap(int(character.get_max_ap() * 0.5))  # Add 50% of max action points
            elif 5 <= result <= 9:
                # Fulfill flow points and action points
                character.add_energy(character.get_max_energy())  # Fill energy points to max
                character.add_ap(character.get_max_ap())  # Fill action points to max
            elif 10 <= result <= 14:
                # Heal health points minorly and fulfill flow points and action points
                character.add_hp(int(character.get_max_hp() * 0.3))  # Add 30% of max health points
                character.add_energy(character.get_max_energy())  # Fill energy points to max
                character.add_ap(character.get_max_ap())  # Fill action points to max
            elif 15 <= result <= 17:
                # Full heal health points and fulfill flow points and action points
                character.add_hp(character.get_max_hp())  # Fill health points to max
                character.add_energy(character.get_max_energy())  # Fill energy points to max
                character.add_ap(character.get_max_ap())  # Fill action points to max
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
                # Also fulfill flow points and action points
                character.add_energy(character.get_max_energy())  # Fill energy points to max
                character.add_ap(character.get_max_ap())  # Fill action points to max

        # Mark the anomaly as known
        self.anomaly.known = True
        self.anomaly.save()
