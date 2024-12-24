from django.db import models

from apps.core.utils.models import BaseModel


class Session(BaseModel):
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE)
    character = models.ForeignKey('character.Character', on_delete=models.CASCADE)


class Campaign(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
