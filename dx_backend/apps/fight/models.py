from django.db import models

from apps.core.utils.models import BaseModel


class Fight(BaseModel):
    position = models.ForeignKey(
        'world.Position',
        on_delete=models.CASCADE,
        related_name='fights'
    )
    attacker = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE,
                                 related_name='fights_initiated')
    defender = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE,
                                 related_name='fights_attacked')

    duel = models.BooleanField(default=False)
    current_round = models.PositiveIntegerField(default=1)
    open = models.BooleanField(default=True)

    created = models.ForeignKey(
        'game.Cycle',
        on_delete=models.CASCADE,
        related_name='fights_started',
        null=True,
        blank=True
    )

    ended_at = models.ForeignKey(
        'game.Cycle',
        on_delete=models.CASCADE,
        related_name='fights_ended',
        null=True,
        blank=True
    )
    pending_join = models.ManyToManyField(
        'character.Character',
        related_name='fights_pending_join',
        blank=True
    )
