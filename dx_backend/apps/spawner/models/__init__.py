from django.db import models
from polymorphic.models import PolymorphicModel

from apps.core.utils.models import BaseModel, TagsDescriptor


class Spawner(BaseModel, PolymorphicModel):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
    position = models.ForeignKey("world.Position", null=True, on_delete=models.SET_NULL, blank=True,
                                 default=None)
    dimension = models.ForeignKey("world.Dimension", on_delete=models.SET_NULL, null=True, blank=True,
                                  default=1)
    is_active = models.BooleanField(default=True)
    campaign = models.ForeignKey('game.Campaign', on_delete=models.CASCADE)

    spawn_limit = models.PositiveIntegerField(default=1)
    respawn_cycles = models.PositiveIntegerField(default=1)

    next_spawn_cycle_number = models.BigIntegerField(default=0,
                                                     help_text='Cycle number when the next spawn should occur',
                                                     editable=False)


class SpawnedEntity(BaseModel):
    spawner = models.ForeignKey(Spawner, on_delete=models.CASCADE, related_name='spawned_entities')
    game_object = models.ForeignKey('core.GameObject', on_delete=models.CASCADE, related_name='spawned_by')
    spawned_at = models.ForeignKey('action.Cycle', null=True, on_delete=models.SET_NULL, blank=True,
                                   default=None)


class NPCSpawner(Spawner):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)
    character_template = models.ForeignKey('character.CharacterTemplate', on_delete=models.CASCADE)
