from django.db import models

from apps.core.models import CharacterStats
from apps.core.utils.models import BaseModel


class Modificator(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.ImageField(upload_to='icons/modificators/', null=True, blank=True)


class StatModificator(BaseModel):
    modificator = models.ForeignKey(Modificator, on_delete=models.CASCADE)
    stat = models.CharField(max_length=255, choices=CharacterStats.choices(), default=CharacterStats.PHYSICAL_STRENGTH)
    value = models.IntegerField(default=0)

class CharacterModificator(BaseModel):
    # character = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE, related_name='modificators')
    character = models.UUIDField()
    modificator = models.ForeignKey(Modificator, on_delete=models.CASCADE)