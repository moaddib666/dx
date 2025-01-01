from django.db import models

from apps.action.models import CharacterAction
from apps.core.models import FightSide, FIGHT_TURN_DURATION_SECONDS
from apps.core.utils.models import BaseModel


class DuelInvitation(BaseModel):
    
    initiator = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE, related_name='duel_invitations_sent')
    target = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE, related_name='duel_invitations_received')

    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    fight = models.ForeignKey('fight.Fight', on_delete=models.CASCADE, null=True, blank=True)


class Fight(BaseModel):
    
    initiator = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE, related_name='fights_initiated')
    target = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE, related_name='fights_attacked')

    is_open = models.BooleanField(default=True)
    is_ended = models.BooleanField(default=False)

    side_a_participants = models.ManyToManyField('character.Character', related_name='fights_side_a', blank=True)
    side_b_participants = models.ManyToManyField('character.Character', related_name='fights_side_b', blank=True)

    current_turn = models.ForeignKey('fight.FightTurn', on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='active_fight')

    def get_character_side(self, character):
        if character in self.side_a_participants.all():
            return FightSide.ATTACKER
        if character in self.side_b_participants.all():
            return FightSide.DEFENDER
        return None


class FightTurn(BaseModel):
    fight = models.ForeignKey('fight.Fight', on_delete=models.CASCADE, related_name='turns')
    is_finished = models.BooleanField(default=False)

    @property
    def duration(self) -> int:
        return FIGHT_TURN_DURATION_SECONDS


class FightTurnAction(CharacterAction):

    turn = models.ForeignKey('fight.FightTurn', on_delete=models.CASCADE, related_name='actions')
    order = models.PositiveIntegerField(blank=True, null=True)
    is_finished = models.BooleanField(default=False)
