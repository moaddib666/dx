from django.db import models

from apps.core.models import CharacterStats
from apps.core.utils.models import BaseModel


class Challenge(BaseModel):
    difficulty = models.PositiveIntegerField(default=12)
    description = models.TextField(blank=True, null=True)
    dice_sides = models.PositiveIntegerField(default=20)
    target = models.ForeignKey(
        "character.Character",
        on_delete=models.CASCADE,
        related_name="challenges"
    )
    outcome = models.ForeignKey(
        "action.DiceRollResult",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="challenges_outcome"
    )
    stat = models.CharField(max_length=255, choices=CharacterStats.choices(), default=CharacterStats.LUCK)
    advantage = models.BooleanField(default=False)
    disadvantage = models.BooleanField(default=False)


class ChallengeModifier(BaseModel):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='challenge_modifiers/', null=True, blank=True)
    value = models.IntegerField()
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="modifiers")
