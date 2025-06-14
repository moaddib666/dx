from apps.action.models import CharacterAction
from apps.core.models import DimensionAnomaly
from apps.game.services.action.base_service import CharacterActionServicePrototype
from apps.game.services.character.core import CharacterService
from apps.game.services.cost import DefaultCostService


class CharacterAnomalyInterractionService(CharacterActionServicePrototype):
    character_svc_cls = CharacterService
    cost_svc = DefaultCostService
    detector_svc_cls = None  # Should be set to the actual anomaly detector service

    def perform(self, action: CharacterAction):
        """
        Use AnomalyDetector(anomaly).detect(charecter: "CharactrerService") to detect anomaly.
        Mark anomaly as known
        """

    def check(self, action: CharacterAction):
        """
        Character must be alive and have enough flow points to interact with anomaly.
        """

    def check_acceptance(self, action: CharacterAction):
        """
        To interact with anomaly, the character must be:
         - alive
         - have flow points > 0
         - have action points > 0
        """
        character = self.character_svc_cls.get_character(action.character)

    def accept(self, action: CharacterAction):
        anomalies = action.targets.instance_of(DimensionAnomaly)

        for anomaly in anomalies:
            if anomaly.known:
                continue

        action.immediate = True
        action.save()
