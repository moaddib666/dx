import uuid
from enum import StrEnum

from django.db import models
from django.utils import timezone


class TagsDescriptor:
    class BaseTags(StrEnum):
        CAMPAIGN_TEMPLATE = "campaign_template"
        CORE_MODEL = "core_model"
        EXCLUDED = "excluded"
        SANDBOX = "sandbox"

    def __init__(self, *tags):
        self.tags = set(tags)

    def __set_name__(self, owner, name):
        self.name = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return getattr(owner, self.name, self.tags)
        return getattr(owner, self.name, self.tags)

    def __set__(self, instance, value):
        # Prevent runtime modification
        raise AttributeError("Tags are read-only")


class Tagged:
    game_tags: TagsDescriptor

    @classmethod
    def has_game_tag(cls, tag: str) -> bool:
        """
        Check if the model has a specific tag.
        :param tag: The tag to check.
        :return: True if the tag is present, False otherwise.
        """
        return tag in cls.game_tags


class BaseModel(Tagged, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
