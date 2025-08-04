import typing as t

from django.db import models

from apps.core import fields
from apps.core.models import ImpactType, ImpactViolationType, CharacterActionType, RollOutcome, \
    CharacterSpecialActionType
from apps.core.utils.models import BaseModel
from apps.school.dto import Cost

if t.TYPE_CHECKING:
    from apps.game.models import Campaign


class CycleManager(models.Manager):
    def current(self, campaign: "Campaign"):
        qs = self.filter(campaign=campaign)
        if qs.count() == 0:
            return self.create(campaign=campaign, number=0)
        return qs.latest('number')

    def next(self, campaign: "Campaign") -> "Cycle":
        current = self.current(campaign=campaign)
        return self.create(campaign=campaign, number=current.number + 1)

    def previous(self, campaign: "Campaign") -> t.Optional["Cycle"]:
        """
        Get the previous cycle for the given campaign.
        If there is no previous cycle, return None.
        """
        current = self.current(campaign=campaign)
        if current.number == 0:
            return None
        return self.filter(campaign=campaign, number__lt=current.number).order_by('-number').first()

    def next_cycle(self, campaign: "Campaign") -> "Cycle":
        """
        Alias for next() for backward compatibility.
        """
        return self.next(campaign=campaign)

    def previous_cycle(self, campaign: "Campaign") -> t.Optional["Cycle"]:
        """
        Alias for previous() for backward compatibility.
        """
        return self.previous(campaign=campaign)


class Cycle(BaseModel):
    """
    A cycle is a representation of a turn in the game. It is a way to keep track of the order of actions in a fight.
    The cycle number is used to determine the order history of actions in a world.
    To get current cycle, use the latest cycle number.
    """
    objects = CycleManager()
    id = models.AutoField(primary_key=True)
    number = models.BigIntegerField(default=0, help_text='Cycle number in the campaign', editable=False)
    campaign = models.ForeignKey('game.Campaign', on_delete=models.CASCADE, related_name='cycles')

    class Meta:
        unique_together = ('number', 'campaign')
        ordering = ['number']

    def __str__(self):
        return f"Cycle {self.number} - {self.campaign.name if self.campaign else 'No Campaign'}"


class CharacterAction(BaseModel):
    ActionType = CharacterActionType
    cycle = models.ForeignKey('action.Cycle', on_delete=models.CASCADE, related_name='actions')
    accepted = models.BooleanField(default=False)
    performed = models.BooleanField(default=False)
    data = models.JSONField(default=dict)
    immediate = models.BooleanField(default=False)
    action_type = models.CharField(max_length=255, choices=ActionType.choices(), default=ActionType.USE_SKILL)

    initiator = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE,
                                  related_name='actions')
    targets = models.ManyToManyField('core.GameObject', related_name='actions_targets', blank=True)

    skill = models.ForeignKey('school.Skill', on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey('items.WorldItem', on_delete=models.CASCADE, null=True, blank=True)
    position = models.ForeignKey('world.Position', on_delete=models.CASCADE, null=True, blank=True)

    fight = models.ForeignKey("fight.Fight", on_delete=models.CASCADE, null=True, blank=True,
                              related_name='actions')
    order = models.FloatField(default=1)

    def accept(self, order: float):
        self.accepted = True
        self.order = order
        if not self.position_id:
            self.position_id = self.initiator.position_id
        self.fight = self.initiator.fight
        self.save(update_fields=['accepted', 'order', 'updated_at', 'fight', 'position_id'])

    def perform(self):
        self.performed = True
        self.save(update_fields=['performed', "updated_at"])

    def __str__(self):
        return f"{self.initiator.name} - {self.action_type}"

    class Meta:
        ordering = ['-cycle', '-order']


class ActionImpact(BaseModel):
    action = models.ForeignKey('action.CharacterAction', on_delete=models.CASCADE, related_name='impacts')
    target = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE,
                               related_name='impacted_by')
    type = models.CharField(choices=ImpactType.choices(), max_length=255)
    violation = models.CharField(max_length=255, choices=ImpactViolationType.choices())
    size = models.IntegerField()
    dice_roll_result = models.ForeignKey('action.DiceRollResult', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.action} - {self.target.name} - {self.type}"


class SpecialAction(models.Model):
    action_type = models.CharField(max_length=255, choices=CharacterSpecialActionType.choices(), primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    immediate = models.BooleanField(default=False, help_text='If true, the action will be performed immediately')
    final = models.BooleanField(default=False, help_text='If true, the action will spend all remaining action points')
    icon = models.ImageField(upload_to='icons/specialActions', null=True, blank=True)
    cost = fields.TypedJSONField(required_type=Cost, many=True, default=list)

    def __str__(self):
        return self.name or str(self.action_type)


class DiceRollResult(BaseModel):
    dice_side = models.IntegerField()
    multiplier = models.FloatField(null=True)
    outcome = models.CharField(max_length=255, choices=RollOutcome.choices())

    def __str__(self):
        return f"{self.dice_side} - {self.outcome}"
