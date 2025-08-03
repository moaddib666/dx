from django.db import models

from apps.core.utils.models import BaseModel


class Fight(BaseModel):
    campaign = models.ForeignKey(
        'game.Campaign',
        on_delete=models.CASCADE,
        related_name='fights'
    )
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
        'action.Cycle',
        on_delete=models.CASCADE,
        related_name='fights_started',
        null=True,
        blank=True
    )

    ended_at = models.ForeignKey(
        'action.Cycle',
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


class CharactersPendingJoinFight(BaseModel):
    """
    Model to track characters pending to join a fight.
    This is used to manage characters that are not yet in a fight but are expected to join.

    This model allows auto joining characters that waits for at least one cycle to join a fight.
    """
    character = models.ForeignKey(
        'character.Character',
        on_delete=models.CASCADE,
        related_name='pending_fights'
    )
    fight = models.ForeignKey(
        Fight,
        on_delete=models.CASCADE,
        related_name='pending_joiners'
    )
    cycle = models.ForeignKey(
        'action.Cycle',
        on_delete=models.CASCADE,
        related_name='pending_join_fights'
    )

    def __str__(self):
        return f"{self.character.name} pending join fight {self.fight.id} in cycle {self.cycle.number}"
