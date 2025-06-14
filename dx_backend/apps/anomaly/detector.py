"""
AnomalyDetector(anomaly).detect(charecter: "CharactrerService") to detect anomaly.
"""
import typing as t
from apps.core.models import DimensionAnomalyEffect
if t.TYPE_CHECKING:
    from apps.core.models import DimensionAnomaly
    from apps.game.services.character.core import CharacterService


class AnomalyDetector:
    def __init__(self, anomaly: "DimensionAnomaly"):
        self.anomaly = anomaly

    def detect(self, character: "CharacterService"):
        if self.anomaly.effect == DimensionAnomalyEffect.Negative:
            # Drop the dice by player d20
            # 18-20 - just decrease action points
            # 15-17 - decrease action points and flow points drastically
            # 10-14 - decrease action points and flow points moderately and remove health points minorly
            # 5-9 - decrease action points and flow points drastically and remove health points moderately
            # 2-4 - decrease action points and flow points drastically and remove health points majorly
            # 1 - kill player by removing all health points all action points and flow points
        if self.anomaly.effect == DimensionAnomalyEffect.Positive:
            # Drop the dice by player d20
            # 1-4 - increase flow points and action points moderately
            # 5-9 - fullfill flow points and action points
            # 10-14 - heal health points minorly and fullfill flow points and action points
            # 15-17 - full heal health points and fullfill flow points and action points
            # 18-20 - Give player with random item of type: `food` or `artifact`

