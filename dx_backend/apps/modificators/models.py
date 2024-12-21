from django.db import models

from apps.core.models import PlayerStat
from apps.core.utils.models import BaseModel


class Modificator(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.ImageField(upload_to='icons/modificators/', null=True, blank=True)


class StatModificator(BaseModel):
    modificator = models.ForeignKey(Modificator, on_delete=models.CASCADE)
    stat = models.CharField(max_length=255, choices=PlayerStat.choices(), default=PlayerStat.PHYSICAL_STRENGTH)
    value = models.IntegerField(default=0)


class PlayerModificator(BaseModel):
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE, related_name='modificators')
    modificator = models.ForeignKey(Modificator, on_delete=models.CASCADE)
