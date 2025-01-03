from django.db import models

from apps.core.models import ImpactViolationType
from apps.core.utils.models import BaseModel


class Shield(BaseModel):
    id = models.CharField(max_length=255, choices=ImpactViolationType.choices, default=ImpactViolationType.NONE,
                          primary_key=True)
    icon = models.ImageField(upload_to='icons/shields/', null=True, blank=True)

    def __str__(self):
        return self.id


class ActiveShieldManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(cycles_left__gt=0)

    def unsafe_all(self):
        return super().get_queryset()

    def inactive(self):
        return self.unsafe_all().filter(cycles_left__lte=0)


class ActiveShield(BaseModel):
    objects = ActiveShieldManager()
    shield = models.ForeignKey(Shield, on_delete=models.CASCADE)
    target = models.ForeignKey(
        'character.Character', to_field='gameobject_ptr',
        on_delete=models.CASCADE,
        related_name='shields'
    )
    cycles_left = models.PositiveIntegerField(default=1)
    health = models.PositiveIntegerField(default=1)
    efficiency = models.FloatField(default=1)
    level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.shield} - {self.target.name}'
