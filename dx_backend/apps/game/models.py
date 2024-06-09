from django.db import models

from apps.core.utils.models import BaseModel


class Session(BaseModel):
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE)
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE)
