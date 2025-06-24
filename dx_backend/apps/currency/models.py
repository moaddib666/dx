from django.db import models

from apps.core.utils.models import BaseModel, TagsDescriptor


class CurrencyToken(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.ImageField(upload_to='icons/currency/', null=True, blank=True)


class CharacterCurrency(BaseModel):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE)

    character = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE,
                                  related_name='tokens')
    currency = models.ForeignKey(CurrencyToken, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
