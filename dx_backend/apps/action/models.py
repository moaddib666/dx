from django.db import models

from apps.core.models import ImpactType, ImpactViolationType, CharacterActionType, RollOutcome
from apps.core.utils.models import BaseModel


class CycleManager(models.Manager):
    def current(self):
        if self.count() == 0:
            return self.next()
        return self.latest('id')

    def next(self):
        return self.create()


class Cycle(BaseModel):
    """
    A cycle is a representation of a turn in the game. It is a way to keep track of the order of actions in a fight.
    The cycle id is used to determine to order history of actions in a world.
    To get current cycle, use the latest cycle id.
    """
    objects = CycleManager()
    id = models.AutoField(primary_key=True)


class CharacterAction(BaseModel):
    ActionType = CharacterActionType

    cycle = models.ForeignKey('action.Cycle', on_delete=models.CASCADE, related_name='actions')
    accepted = models.BooleanField(default=False)
    performed = models.BooleanField(default=False)
    data = models.JSONField(default=dict)

    action_type = models.CharField(max_length=255, choices=ActionType.choices(), default=ActionType.USE_SKILL)

    initiator = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE,
                                  related_name='actions')
    targets = models.ManyToManyField('core.GameObject', related_name='actions_targets', blank=True)

    skill = models.ForeignKey('school.Skill', on_delete=models.CASCADE, null=True, blank=True)
    position = models.ForeignKey('world.Position', on_delete=models.CASCADE, null=True, blank=True)

    def accept(self):
        self.accepted = True
        self.save(update_fields=['accepted'])

    def perform(self):
        self.performed = True
        self.save(update_fields=['performed'])

    def __str__(self):
        return f"{self.initiator.name} - {self.action_type}"

    class Meta:
        ordering = ['-cycle', '-created_at']


class ActionImpact(BaseModel):
    action = models.ForeignKey('action.CharacterAction', on_delete=models.CASCADE, related_name='impacts')
    target = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE, related_name='impacted_by')
    type = models.CharField(choices=ImpactType.choices(), max_length=255)
    violation = models.CharField(max_length=255, choices=ImpactViolationType.choices())
    size = models.IntegerField()
    dice_roll_result = models.ForeignKey('action.DiceRollResult', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.action} - {self.target.name} - {self.type}"


class DiceRollResult(BaseModel):
    dice_side = models.IntegerField()
    multiplier = models.FloatField(null=True)
    outcome = models.CharField(max_length=255, choices=RollOutcome.choices())

    def __str__(self):
        return f"{self.dice_side} - {self.outcome}"
