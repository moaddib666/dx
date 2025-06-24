from django.db import models

from apps.core.models import GameObject, ItemType
from apps.core.utils.models import BaseModel, TagsDescriptor


class ItemsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(canonical=True)

    def all(self):
        return super().all()

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class Item(BaseModel):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    icon = models.ImageField(upload_to='icons/items/', null=True, blank=True)
    type = models.CharField(max_length=255, choices=ItemType.choices, default=ItemType.MISC)

    charges = models.IntegerField(default=1)
    weight = models.FloatField(default=0.0)
    visibility = models.FloatField(default=1.0)  # 0.0 - 1.0 (0% - 100%)

    skill = models.ForeignKey('school.Skill', on_delete=models.SET_NULL, null=True, blank=True)
    effect = models.ForeignKey('effects.Effect', on_delete=models.SET_NULL, null=True, blank=True)

    base_price = models.PositiveIntegerField(default=1)
    canonical = models.BooleanField(default=True)

    campaign = models.ForeignKey('game.Campaign', on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.name} ({self.type})"


class WorldItem(GameObject):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    charges_left = models.PositiveIntegerField(default=1)
    visibility = models.FloatField(default=1.0)  # 0.0 - 1.0 (0% - 100%)

    def __str__(self):
        return f"{self.item.name}"


class CharacterItem(BaseModel):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
    character = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE,
                                  related_name='equipped_items')
    world_item = models.ForeignKey(WorldItem, on_delete=models.CASCADE)

    @property
    def visibility(self) -> float:
        return self.world_item.visibility
