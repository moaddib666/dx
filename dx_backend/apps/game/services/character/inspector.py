import logging

from apps.character.models import Character
from apps.core.models import CharacterInspectInfo, AttributeHolder, AttributeType
from .core import CharacterService


class CharacterInspectorService:
    logger = logging.getLogger("game.services.character.inspector")

    def __init__(self, character_svc_cls: type[CharacterService] = None):
        self.character_svc_cls = character_svc_cls or CharacterService

    def inspect(self, initiator: Character, target: Character) -> CharacterInspectInfo:
        self.logger.info(f"Starting inspection: initiator={initiator.id}, target={target.id}")

        initiator_svc = self.character_svc_cls(initiator)
        target_svc = self.character_svc_cls(target)

        initiator_dice_svc = initiator_svc.get_dice_service()(sides=20)
        target_dice_svc = target_svc.get_dice_service()(sides=20)

        initiator_dice_roll = initiator_dice_svc.roll()
        target_dice_roll = target_dice_svc.roll()

        self.logger.debug(f"Initiator dice roll: {initiator_dice_roll}, Target dice roll: {target_dice_roll}")

        result = self.get_empty_result(target_svc)

        if initiator_dice_roll <= 1:
            self.logger.info("Inspection failed: initiator dice roll was 1 or lower.")
            return result

        if target_dice_roll >= 20:
            self.logger.info("Inspection failed: target dice roll was 20 or higher.")
            return result

        # 0 is the maximum rank grade and 9 is the minimum rank grade
        # initiator 7 target 9 => initiator is 2 rank ahead the target
        # initiator 0 target 9 => initiator is 9 rank ahead the target
        # initiator 9 target 9 => initiator is 0 rank ahead the target
        # initiator 9 target 8 => initiator is 1 rank behind the target and it's not allowed to inspect

        # (target - initiator) = rank_diff
        # 9 - 7 = 2
        # 7 - 9 = -2
        rank_diff = target_svc.rank_grade - initiator_svc.rank_grade

        if rank_diff < 0 and initiator_dice_roll != 20:
            self.logger.info("Inspection failed: initiator rank is lower than target rank and dice roll is not 20.")
            return result

        self.logger.info("Inspection succeeded: adding rank grade and attributes.")
        self.add_rank_grade(target_dice_roll, result, initiator_svc, target_svc)
        self.add_attributes(target_dice_roll, result, initiator_svc, target_svc)
        return result

    def get_empty_result(self, target_svc: CharacterService) -> CharacterInspectInfo:
        self.logger.debug(f"Generating empty inspection result for target: {target_svc.model.pk}")
        return CharacterInspectInfo(
            id=target_svc.model.pk,
            name=target_svc.model.name,
            attributes=[],
            dimension=target_svc.model.dimension_id,
            rank_grade=None,
            path=None
        )

    def add_rank_grade(self, roll_result: int, result: CharacterInspectInfo, initiator_svc: CharacterService,
                       target_svc: CharacterService):
        if roll_result < 5:
            self.logger.debug(f"Cannot add rank grade: roll result {roll_result} is less than 5.")
            return

        result.rank_grade = target_svc.rank_grade
        self.logger.debug(f"Added rank grade: {result.rank_grade}")
        return result

    def add_attributes(self, roll_result: int, result: CharacterInspectInfo, initiator_svc: CharacterService,
                       target_svc: CharacterService):
        if roll_result < 10:
            self.logger.debug(f"Cannot add attributes: roll result {roll_result} is less than 10.")
            return

        energy_attr = target_svc.get_attribute(AttributeType.ENERGY)
        self.logger.debug(f"Adding energy attribute only (roll result: {roll_result}).")
        result.attributes = [energy_attr]

        health_attr = target_svc.get_attribute(AttributeType.HEALTH)
        if roll_result < 13:
            return result

        self.logger.debug(f"Adding attributes: energy and health (roll result: {roll_result}).")
        result.attributes = [energy_attr, health_attr]


default_inspector = CharacterInspectorService()
