import logging
import typing as t

from django.db import models

from apps.game.services.clone.base import Dependency

logger = logging.getLogger("apps.game.services.clone")


class UnexpectedDependencyError(Exception):
    """
    Exception raised when we have dependency that we did not fit the current instance model.
    """

    def __init__(self, dependency: Dependency):
        super().__init__(f"Unexpected dependency: {dependency}")
        self.dependency = dependency


class RelationUpdater(t.Protocol):
    """
    Protocol for updating relations in cloned instances.
    """

    def can_fix(self, dependency: Dependency) -> bool:
        """
        Check if the updater can handle the given dependency.
        This method should be implemented by concrete relation updaters.
        """
        raise NotImplementedError("This method should be implemented by concrete relation updaters.")

    def fix(self, dependency: Dependency) -> None:
        """
        Update the relation in the cloned instance based on the dependency.
        This method should be implemented by concrete relation updaters.
        """
        raise NotImplementedError("This method should be implemented by concrete relation updaters.")


class OneToOneUpdater(RelationUpdater):
    """
    Updater for OneToOne relationships.
    """

    def can_fix(self, dependency: Dependency) -> bool:
        return dependency.reverse and isinstance(dependency.field, models.OneToOneRel)

    def fix(self, dependency: Dependency) -> None:
        """
        Update the target instance's relation based on the dependency.
        """
        logger.debug("Updating OneToOne relation for %s", dependency.target)
        target_model = dependency.field.model
        if isinstance(dependency.target, target_model):
            setattr(dependency.source, dependency.field.remote_field.name, dependency.target)
        elif isinstance(dependency.source, target_model):
            setattr(dependency.target, dependency.field.remote_field.name, dependency.source)
        else:
            raise UnexpectedDependencyError(dependency)


class ManyToOneUpdater(RelationUpdater):
    """
    Updater for ManyToOne relationships.
    """

    def can_fix(self, dependency: Dependency) -> bool:
        return dependency.reverse and isinstance(dependency.field, models.ManyToOneRel)

    def fix(self, dependency: Dependency) -> None:
        """
        Update the target instance's relation based on the dependency.
        """
        logger.debug("Updating ManyToOne relation for %s", dependency.target)
        setattr(dependency.target, dependency.field.remote_field.name, dependency.source)


class ManyToManyUpdater(RelationUpdater):
    """
    Updater for ManyToMany relationships.
    """

    def can_fix(self, dependency: Dependency) -> bool:
        return dependency.reverse and isinstance(dependency.field, models.ManyToManyRel)

    def fix(self, dependency: Dependency) -> None:
        """
        Update the target instance's relation based on the dependency.
        """
        logger.debug("Updating ManyToMany relation for %s", dependency.target)
        related_manager = getattr(dependency.target, dependency.field.name)
        related_manager.add(dependency.source)


class CompositeUpdater(RelationUpdater):
    """
    Updater for composite relationships that can handle multiple types of relations.
    """

    def __init__(self, updaters: t.List[RelationUpdater]):
        self.updaters = updaters

    def can_fix(self, dependency: Dependency) -> bool:
        return any(updater.can_fix(dependency) for updater in self.updaters)

    def fix(self, dependency: Dependency) -> None:
        for updater in self.updaters:
            if updater.can_fix(dependency):
                updater.fix(dependency)
                return
        raise UnexpectedDependencyError(dependency)


def get_default_relation_updater() -> RelationUpdater:
    """
    Create a default updater that can handle OneToOne, ManyToOne, and ManyToMany relationships.
    """
    return CompositeUpdater([
        OneToOneUpdater(),
        ManyToOneUpdater(),
        ManyToManyUpdater()
    ])
