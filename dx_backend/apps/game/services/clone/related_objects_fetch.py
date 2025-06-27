import logging
import typing as t

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

logger = logging.getLogger("apps.game.services.clone")


class UnsupportedFieldTypeError(Exception):
    """
    Exception raised when an unsupported field type is encountered.
    """

    def __init__(self, field: t.Any):
        super().__init__(f"Unsupported field type: {type(field)} for field {field}")
        self.field = field


class FieldRelationFetcher(t.Protocol):

    def can_fetch(self, field: t.Any) -> bool:
        """
        Check if the field can be fetched.
        """
        pass

    def fetch(self, instance: models.Model, field: t.Any) -> t.Iterable[models.Model]:
        """
        Fetch the related objects for the given field.
        """
        pass


class ManyToOneFetcher(FieldRelationFetcher):
    """
    Fetcher for ManyToOne relationships.
    """

    def can_fetch(self, field: t.Any) -> bool:
        return isinstance(field, models.ManyToOneRel)

    def fetch(self, instance: models.Model, field: t.Any) -> t.Iterable[models.Model]:
        """
        Fetch related objects for ManyToOne relationships.
        """
        logger.debug("Fetching ManyToOne related objects for %s using field %s", instance, field)
        related_manager = getattr(instance, field.get_accessor_name())
        return related_manager.all()


class ManyToManyFetcher(FieldRelationFetcher):
    """
    Fetcher for ManyToMany relationships.
    """

    def can_fetch(self, field: t.Any) -> bool:
        return isinstance(field, models.ManyToManyRel)

    def fetch(self, instance: models.Model, field: t.Any) -> t.Iterable[models.Model]:
        """
        Fetch related objects for ManyToMany relationships.
        """
        logger.debug("Fetching ManyToMany related objects for %s using field %s", instance, field)
        related_manager = getattr(instance, field.get_accessor_name())
        return related_manager.all()


class OneToOneFetcher(FieldRelationFetcher):
    """
    Fetcher for OneToOne relationships.
    """

    def can_fetch(self, field: t.Any) -> bool:
        return isinstance(field, models.OneToOneRel)

    def fetch(self, instance: models.Model, field: t.Any) -> t.Iterable[models.Model]:
        """
        Fetch related objects for OneToOne relationships.
        """
        logger.debug("Fetching OneToOne related object for %s using field %s", instance, field)
        try:
            related_instance = getattr(instance, field.get_accessor_name(), None)
        except ObjectDoesNotExist:
            logger.warning("No related object found for %s using field %s", instance, field)
            return []
        return [related_instance] if related_instance else []


class CompositeFetcher(FieldRelationFetcher):
    """
    Fetcher for composite relationships that can handle multiple field types.
    """

    def __init__(self, fetchers: t.Iterable[FieldRelationFetcher]):
        self.fetchers = fetchers

    def can_fetch(self, field: t.Any) -> bool:
        return any(fetcher.can_fetch(field) for fetcher in self.fetchers)

    def fetch(self, instance: models.Model, field: t.Any) -> t.Iterable[models.Model]:
        for fetcher in self.fetchers:
            if fetcher.can_fetch(field):
                return fetcher.fetch(instance, field)
        raise UnsupportedFieldTypeError(field)


def get_default_relations_fetcher() -> FieldRelationFetcher:
    """
    Create a default fetcher that can handle ManyToOne, ManyToMany, and OneToOne relationships.
    """
    return CompositeFetcher([
        OneToOneFetcher(),
        ManyToOneFetcher(),
        ManyToManyFetcher(),
    ])
