from django.db import models

from apps.core.models import ImpactType, ImpactViolationType, CharacterActionType, RollOutcome
from apps.core.utils.models import BaseModel


class CharacterAction(BaseModel):

    ActionType = CharacterActionType
    action_type = models.CharField(max_length=255, choices=ActionType.choices(), default=ActionType.USE_SKILL)
    initiator = models.ForeignKey('character.Character', on_delete=models.CASCADE, related_name='actions')
    targets = models.ManyToManyField('character.Character', related_name='actions_targets')

    skill = models.ForeignKey('school.Skill', on_delete=models.CASCADE, null=True, blank=True)
    target_dimension = models.ForeignKey('world.Dimension', on_delete=models.CASCADE, null=True, blank=True)
    target_location = models.ForeignKey('world.Location', on_delete=models.CASCADE, null=True, blank=True)


class ActionImpact(BaseModel):
    action = models.ForeignKey('action.CharacterAction', on_delete=models.CASCADE, related_name='impacts')
    target = models.ForeignKey('character.Character', on_delete=models.CASCADE, related_name='impacted_by')
    type = models.CharField(choices=ImpactType.choices(), max_length=255)
    violation = models.CharField(max_length=255, choices=ImpactViolationType.choices())
    size = models.IntegerField()
    dice_roll_result = models.ForeignKey('action.DiceRollResult', on_delete=models.CASCADE, null=True)


class DiceRollResult(BaseModel):
    dice_side = models.IntegerField()
    multiplier = models.FloatField(null=True)
    outcome = models.CharField(max_length=255, choices=RollOutcome.choices())
