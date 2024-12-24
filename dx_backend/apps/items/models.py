from django.db import models

from apps.core.utils.models import BaseModel


class ItemsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(canonical=True)

    def all(self):
        return super().all()

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Item(BaseModel):
    class ItemType(models.TextChoices):
        WEAPON = 'weapon'
        ARMOR = 'armor'
        POTION = 'artifact'
        FOOD = 'amulet'
        MATERIAL = 'material'
        QUEST = 'quest'
        MISC = 'misc'

    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.ImageField(upload_to='icons/items/', null=True, blank=True)
    type = models.CharField(max_length=255, choices=ItemType.choices, default=ItemType.MISC)
    weight = models.FloatField()

    ap_cost = models.IntegerField(default=1)
    hp_cost = models.IntegerField(default=0)
    ep_cost = models.IntegerField(default=0)

    once_per_fight = models.BooleanField(default=False)
    once_per_turn = models.BooleanField(default=False)
    once = models.BooleanField(default=False)

    canonical = models.BooleanField(default=False)


class CharacterItem(BaseModel):
    character = models.ForeignKey('character.Character', on_delete=models.CASCADE, related_name='equipped_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
