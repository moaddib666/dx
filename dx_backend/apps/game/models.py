from django.db import models

from apps.core.utils.models import BaseModel, TagsDescriptor


class Session(BaseModel):
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE)
    character = models.ForeignKey('character.Character', to_field='gameobject_ptr', on_delete=models.CASCADE)


class Campaign(BaseModel):
    game_tags = TagsDescriptor(TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE, TagsDescriptor.BaseTags.CORE_MODEL)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"
