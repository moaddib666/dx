from django.db import models

from apps.core.utils.models import BaseModel


class GalleryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(canonical=True)

    def all(self):
        return super().all()

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)

    def not_canonical(self):
        return super().get_queryset().filter(canonical=False)


class Art(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='art/')
    canonical = models.BooleanField(default=False)

    objects = GalleryManager()

    def __str__(self):
        return self.name
