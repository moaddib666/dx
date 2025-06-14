from apps.action.models import CharacterAction
from apps.core.models import DimensionAnomaly, AttributeType
from apps.game.exceptions import GameLogicException
from apps.game.services.action.base_service import CharacterActionServicePrototype
from apps.game.services.anomaly.detector import AnomalyDetector
from apps.game.services.character.character_items import CharacterItemsService
from apps.game.services.character.core import CharacterService
from apps.game.services.cost import DefaultCostService


class CharacterAnomalyInteractionService(CharacterActionServicePrototype):
    character_svc_cls = CharacterService
    cost_svc = DefaultCostService
    detector_svc_cls = AnomalyDetector
    items_svc_cls = CharacterItemsService

    def perform(self, action: CharacterAction):
        """
        Use AnomalyDetector(anomaly).detect(charecter: "CharactrerService") to detect anomaly.
        Mark anomaly as known
        """
        character_svc = self.character_svc_cls(action.initiator)
        anomalies = action.targets.instance_of(DimensionAnomaly)
        for anomaly in anomalies:
            self.detector_svc_cls(anomaly).detect(character_svc)

    def check(self, action: CharacterAction):
        """
        Character must be alive and have enough flow points to interact with anomaly.
        """
        character_svc = self.character_svc_cls(action.initiator)

        if character_svc.is_knocked_out():
            raise GameLogicException("Character is knocked out and cannot interact with anomaly")

        if character_svc.get_attribute_value(AttributeType.ENERGY) <= 0:
            raise GameLogicException("Character does not have enough flow points to interact with anomaly")

        if character_svc.get_attribute_value(AttributeType.ACTION_POINTS) <= 0:
            raise GameLogicException("Character does not have enough action points to interact with anomaly")

    def check_acceptance(self, action: CharacterAction):
        """
        To interact with anomaly, the character must be:
         - alive
         - have flow points > 0
         - have action points > 0
        """
        character_svc = self.character_svc_cls(action.initiator)

        if character_svc.is_knocked_out():
            raise GameLogicException("Character is knocked out and cannot interact with anomaly")

        if character_svc.get_attribute_value(AttributeType.ENERGY) <= 0:
            raise GameLogicException("Character does not have enough flow points to interact with anomaly")

        if character_svc.get_attribute_value(AttributeType.ACTION_POINTS) <= 0:
            raise GameLogicException("Character does not have enough action points to interact with anomaly")
        if not action.targets.exists():
            raise GameLogicException("No anomalies to interact with")
        for anomaly in action.targets.instance_of(DimensionAnomaly):
            if anomaly.known:
                raise GameLogicException("Anomaly is already known and cannot be interacted with again")
        return True

    def accept(self, action: CharacterAction):
        action.immediate = True
        action.save()
        return True
