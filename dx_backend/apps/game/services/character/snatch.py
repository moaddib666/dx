import logging
import random

from apps.character.models import Character
from apps.core.models import SnatchResult, CharacterStats
from .character_items import default_items_svc_factory
from .core import CharacterService


class CharacterSnatchService:
    logger = logging.getLogger("game.services.character.snatch")
    item_svc_factory = default_items_svc_factory

    def __init__(self, character_svc_cls: type[CharacterService] = None):
        self.character_svc_cls = character_svc_cls or CharacterService

    def snatch(self, initiator: Character, target: Character) -> SnatchResult:
        """
        Attempt to snatch items from a target character.
        Returns a SnatchResult indicating success and a list of snatched items.
        """
        self.logger.info(f"Snatch attempt initiated by {initiator.id} targeting {target.id}.")

        initiator_svc = self.character_svc_cls(initiator)
        target_svc = self.character_svc_cls(target)

        # Roll dice for both characters
        initiator_dice_svc = initiator_svc.get_dice_service()(sides=20)
        target_dice_svc = target_svc.get_dice_service()(sides=20)

        initiator_dice_roll = initiator_dice_svc.roll()
        target_dice_roll = target_dice_svc.roll()

        self.logger.info(
            f"Snatch dice rolls: Initiator={initiator_dice_roll}, Target={target_dice_roll}"
        )

        # Check if the target is knocked out or rolls are favorable
        if not target_svc.is_knocked_out():
            if initiator_dice_roll != 20 and target_dice_roll != 1:
                self.logger.warning(
                    "Snatch failed: Target is not knocked out and rolls are unfavorable."
                )
                return SnatchResult(success=False, snatched=[], discovered=[], target=target.id)

        if initiator_dice_roll <= 1:
            self.logger.warning("Snatch failed: Initiator rolled a critical failure.")
            return SnatchResult(success=False, snatched=[], discovered=[], target=target.id)
        if target_dice_roll == 20:
            self.logger.warning("Snatch failed: Target rolled a critical success.")
            return SnatchResult(success=False, snatched=[], discovered=[], target=target.id)

        # Fetch items from the target
        target_items_svc = self.item_svc_factory.from_character(target)
        target_items = target_items_svc.get_visible_items()

        discovered_items = []
        for item in target_items:
            visibility = item.visibility  # Assume visibility is a float (0.0 to 1.0)
            snatch_probability = self.calculate_snatch_probability(
                visibility,
                initiator_svc,
                target_svc,
                initiator_dice_roll,
                target_dice_roll
            )

            self.logger.debug(
                f"Evaluating item {item.id}: Visibility={visibility}, "
                f"Snatch Probability={snatch_probability}%"
            )

            # Determine if the item is snatched
            if random.uniform(0, 100) <= snatch_probability:
                self.logger.info(f"Item {item.id} successfully snatched.")
                discovered_items.append(item)
            else:
                self.logger.debug(f"Item {item.id} not snatched.")

        # Determine maximum items snatched based on dice roll
        max_items = self.calculate_max_snatch_items_count(initiator_dice_roll)
        snatched_items = discovered_items[:max_items]

        # Final success determination
        success = bool(snatched_items)
        if success:
            initiator_items_svc = self.item_svc_factory.from_character(initiator)
            for item in snatched_items:
                world_item = target_items_svc.remove_item(item)
                self.logger.info(f"Adding snatched item {world_item.id} to initiator.")
                initiator_items_svc.add_item(world_item)

        self.logger.info(
            f"Snatch result: {'Success' if success else 'Failure'}, "
            f"Snatched Items={len(snatched_items)}, Discovered Items={len(discovered_items)}"
        )
        return SnatchResult(
            success=success,
            snatched=[item.world_item_id for item in snatched_items],
            discovered=[item.world_item_id for item in discovered_items],
            target=target.id
        )

    def calculate_max_snatch_items_count(self, dice_result: int) -> int:
        """
        Determine the maximum number of items that can be snatched based on the dice roll.
        """
        if dice_result == 20:
            return 3
        if dice_result >= 15:
            return 2
        return 1

    def calculate_snatch_probability(
            self,
            visibility: float,
            initiator_svc: CharacterService,
            target_svc: CharacterService,
            initiator_dice_roll: int,
            target_dice_roll: int
    ) -> float:
        """
        Calculate the probability of successfully snatching an item.
        """
        # Fetch character stats
        initiator_luck = initiator_svc.get_stat(CharacterStats.LUCK)
        target_luck = target_svc.get_stat(CharacterStats.LUCK)

        # Differences in dice rolls and luck
        dice_diff = initiator_dice_roll - target_dice_roll
        luck_diff = initiator_luck - target_luck

        # Log initial values for debugging
        self.logger.debug(
            f"Calculating Snatch Probability: Visibility={visibility}, "
            f"Initiator Luck={initiator_luck}, Target Luck={target_luck}, "
            f"Initiator Dice Roll={initiator_dice_roll}, Target Dice Roll={target_dice_roll}, "
            f"Dice Diff={dice_diff}, Luck Diff={luck_diff}"
        )

        if visibility == 0:
            self.logger.debug("Visibility is 0; item cannot be snatched.")
            return 0

        # Base visibility as a percentage
        snatch_probability = visibility * 100

        # Adjustments for luck difference (smoothed scaling)
        luck_adjustment = luck_diff ** 0.24 if luck_diff > 0 else -(abs(luck_diff) ** 0.24)
        snatch_probability += luck_adjustment

        # Adjustments for dice difference (linear scaling)
        dice_adjustment = dice_diff * 0.3
        snatch_probability += dice_adjustment

        # Clamp probability to valid range [0, 100]
        snatch_probability = max(0, min(snatch_probability, 100))

        # Log final probability calculation
        self.logger.debug(
            f"Snatch Probability Calculation: Base Visibility={visibility * 100:.1f}%, "
            f"Luck Adjustment={luck_adjustment:.2f}, Dice Adjustment={dice_adjustment:.2f}, "
            f"Final Probability={snatch_probability:.1f}%"
        )

        return snatch_probability


default_snatcher = CharacterSnatchService()
