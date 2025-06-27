import copy
import logging
import typing as t

from django.db.models import Model, OneToOneField
from polymorphic.models import PolymorphicModel

from apps.game.services.clone.base import Dependency

logger = logging.getLogger("apps.game.services.clone")


class CloneService(t.Protocol):
    """
    Protocol for clone services that handle cloning of game objects.
    """
    __repository__: dict[Model, Model]

    def __init__(self, **kwargs: t.Any) -> None:
        """
        Initialize the clone service with an empty repository.
        This method should be implemented by concrete clone services.
        """
        self.__repository__ = {}

    def clone_model(self, instance: Model, **kwargs: t.Any) -> Model:
        """
        Clone the given model instance.
        This method should be implemented by concrete clone services.
        """
        new_instance = self._clone_model(instance, **kwargs)
        self.__repository__[instance] = new_instance  # Store the cloned instance in the repository
        return new_instance

    def _clone_model(self, instance: Model, **kwargs: t.Any) -> Model:
        """
        Clone the given model instance without storing it in the repository.
        This method is used internally and should not be called directly.
        """
        new_instance = copy.deepcopy(instance)
        new_instance.pk = None
        return new_instance

    def clone(self, dependency: Dependency, **kwargs: t.Any) -> Dependency:
        """
        Clone the target instance based on the new source instance.
        This method should be implemented by concrete clone services.
        """
        if not self.has_cloned(dependency.source):
            raise ValueError(
                f"Cannot clone {dependency.target.__class__.__name__} {dependency.target.pk} "
                f"because source instance {dependency.source.__class__.__name__} {dependency.source.pk} "
                "has not been cloned yet."
            )
        new_target_instance = self.get_cloned(dependency.target)
        if not new_target_instance:
            new_target_instance = self.clone_model(dependency.target, **kwargs)

        new_instance = dependency.clone(
            source=self.get_cloned(dependency.source),
            target=new_target_instance,
        )
        return new_instance

    def has_cloned(self, instance: Model) -> bool:
        """
        Check if the instance has already been cloned.
        This method should be implemented by concrete clone services.
        """
        return instance in self.__repository__

    def get_cloned(self, instance: Model) -> Model:
        """
        Retrieve the cloned instance from the repository.
        This method should be implemented by concrete clone services.
        """
        return self.__repository__.get(instance, None)


class DefaultCloneService(CloneService):
    """
    Default implementation of the CloneService protocol.
    This service uses a simple in-memory repository to store cloned instances.
    """


class PolymorphicCloneService(DefaultCloneService):
    """
    Polymorphic implementation of the CloneService protocol.
    This service can handle cloning of instances with polymorphic relations.
    """

    def _clone_model(self, instance: Model, **kwargs: t.Any) -> Model:
        new_instance = super()._clone_model(instance, **kwargs)
        if isinstance(new_instance, PolymorphicModel):
            setattr(new_instance, getattr(new_instance, 'polymorphic_primary_key_name'), None)
            # Clean up polymorph pointers
            for field in new_instance._meta.get_fields(include_parents=True):
                if not isinstance(field, OneToOneField):
                    continue
                if not isinstance(instance, field.related_model):
                    continue
                setattr(new_instance, field.attname, None)

        return new_instance
