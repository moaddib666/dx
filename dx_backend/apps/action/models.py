from django.db import models
from apps.core.utils.models import BaseModel


class PlayerAction(BaseModel):

    class ActionType(models.TextChoices):
        use_skill = 'use_skill'
        use_item = 'use_item'
        dimension_shift = 'dimension_shift'
        change_position = 'change_position'
        start_dialogue = 'start_dialogue'
        make_duel_invitation = 'make_duel_invitation'
        accept_duel_invitation = 'accept_duel_invitation'
        reject_duel_invitation = 'reject_duel_invitation'
        start_fight = 'start_fight'

    action_type = models.CharField(max_length=255, choices=ActionType.choices, default=ActionType.use_skill)
    initiator = models.ForeignKey('player.Player', on_delete=models.CASCADE, related_name='actions')
    targets = models.ManyToManyField('player.Player', related_name='actions_targets')

    skill = models.ForeignKey('school.Skill', on_delete=models.CASCADE, null=True, blank=True)
    target_dimension = models.ForeignKey('world.Dimension', on_delete=models.CASCADE, null=True, blank=True)
    target_location = models.ForeignKey('world.Location', on_delete=models.CASCADE, null=True, blank=True)

    impact = models.JSONField(default=dict)


