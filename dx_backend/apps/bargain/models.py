from django.db import models

from apps.core.utils.models import BaseModel


class Bargain(BaseModel):
    side_a = models.ForeignKey('character.Character', on_delete=models.SET_NULL, related_name='bargain_initiator',
                               null=True, blank=True)
    side_b = models.ForeignKey('character.Character', on_delete=models.SET_NULL, related_name='bargain_receiver',
                               null=True, blank=True)

    side_a_offered_items = models.ManyToManyField('bargain.OfferedItem', related_name='side_a_offered_items', blank=True)
    side_b_offered_items = models.ManyToManyField('bargain.OfferedItem', related_name='side_b_offered_items', blank=True)

    side_a_accepted = models.BooleanField(default=False)
    side_b_accepted = models.BooleanField(default=False)

    cancelled = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)


class OfferedItem(BaseModel):
    item = models.ForeignKey('items.WorldItem', on_delete=models.CASCADE)
    bargain = models.ForeignKey('bargain.Bargain', on_delete=models.CASCADE)
