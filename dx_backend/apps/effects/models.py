from django.db import models

from apps.core.models import EffectType
from apps.core.utils.models import BaseModel


class Effect(BaseModel):
    id = models.CharField(max_length=255, choices=EffectType.choices, default=EffectType.NONE, primary_key=True)
    icon = models.ImageField(upload_to='icons/effects/', null=True, blank=True)
    permanent = models.BooleanField(default=False)
    ends_in = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.id


class ActiveEffectQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def inactive(self):
        return self.filter(active=False)


class ActiveEffectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)

    def unsafe_all(self):
        return super().get_queryset()

    def inactive(self):
        return self.unsafe_all().filter(active=False)


class ActiveEffect(BaseModel):
    objects = ActiveEffectManager()
    effect = models.ForeignKey(Effect, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(default=0)
    impact = models.JSONField(default=dict, null=True, blank=True)
    # Fixme - on reverse relation .effects.all() returns all effects, not only active
    target = models.ForeignKey(
        'character.Character',
        on_delete=models.CASCADE,
        related_name='effects'

    )
    active = models.BooleanField(default=True)

    _data = models.JSONField(default=dict, null=True, blank=True)

    def get_internal_data(self) -> dict:
        return self._data

    def __str__(self):
        return f'{self.effect} - {self.target.name}'
