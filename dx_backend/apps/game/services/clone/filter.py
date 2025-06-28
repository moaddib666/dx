import typing as t

from apps.core.utils.models import TagsDescriptor


class ModelFilter(t.Protocol):

    def filter(self, model: t.Any) -> bool:
        """
        Filter method to determine if the instance should be included.
        This method should be implemented by concrete instance filters.
        """
        raise NotImplementedError("This method should be implemented by concrete instance filters.")


class TaggedContextFilter(ModelFilter):
    """
    Filter for campaign context instances.
    This filter checks if the instance is part of a campaign context.
    """

    def __init__(self, tag: TagsDescriptor.BaseTags):
        self.tag = tag

    def filter(self, model: t.Any) -> bool:
        """
        Check if the instance is part of a campaign context.
        """
        game_tags = getattr(model, 'game_tags', [])
        return self.tag in game_tags
