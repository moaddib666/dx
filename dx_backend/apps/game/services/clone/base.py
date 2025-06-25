import dataclasses
import logging
import typing as t


class AlreadyClonedError(Exception):
    pass


class CannotCloneError(Exception):
    pass


class DependencySetter(t.Protocol):
    """
    Protocol for a setter that can assign a cloned dependency to a target instance.
    """

    def __call__(self, parent_instance: t.Any, child_instance: t.Any) -> None:
        """
        Set the dependency on the target instance.
        :param target_instance: The instance to which the dependency should be assigned.
        :param dependency_instance: The instance that is being assigned as a dependency.
        """
        raise NotImplementedError("set_dependency method must be implemented by subclasses.")


class CloneLogger(t.Protocol):
    """
    Protocol that has model to id log so that we do not clone the same instance multiple times.
    """
    history: t.Dict[t.Any, t.Set[str]]

    def cloned(self, model_instance: t.Any, instance_id: str) -> None:
        """
        Log the cloning of a model instance with its ID.
        :param model_instance: The instance that is being cloned.
        :param instance_id: The unique identifier of the instance.
        """
        if model_instance not in self.history:
            self.history[model_instance] = set()
        self.history[model_instance].add(instance_id)

    def is_cloned(self, model_instance: t.Any, instance_id: str) -> bool:
        """
        Check if a model instance with the given ID has already been cloned.
        :param model_instance: The instance to check.
        :param instance_id: The unique identifier of the instance.
        :return: True if the instance has been cloned, False otherwise.
        """
        return model_instance in self.history and instance_id in self.history[model_instance]


@dataclasses.dataclass
class Dependency:
    """
    Represents a dependency of a model instance that can be cloned.
    This is used to track dependencies that need to be cloned alongside the parent instance.

    :param instance: The instance that is a dependency of any other model instance.
    :param assigner: A callable that can be used to assign the cloned dependency to the target instance.
    """
    instance: t.Any
    assigner: t.Callable[[t.Any, t.Any], None] = None

    def __hash__(self):
        return hash(self.instance)

    def __eq__(self, other):
        if not isinstance(other, Dependency):
            return NotImplemented
        return self.instance == other.instance and self.assigner == other.assigner

    def __repr__(self):
        return f"Dependency(instance={self.instance}, assigner={self.assigner})"

    def __str__(self):
        return f"Dependency: {self.instance} with assigner {self.assigner.__name__ if self.assigner else 'None'}"


class FilterDependency(t.Protocol):

    def __call__(self, dependency: Dependency) -> bool:
        """
        Filter dependencies based on a condition.
        :param dependency: The dependency to check.
        :return: True if the dependency should be included, False otherwise.
        """
        raise NotImplementedError("FilterDependency method must be implemented by subclasses.")


class AcceptAllDependencies(FilterDependency):
    """
    A filter that accepts all dependencies without any condition.
    This is useful when you want to include all discovered dependencies.
    """

    def __call__(self, dependency: Dependency) -> bool:
        return True  # Accept all dependencies


class DependencyDiscoveryService(t.Protocol):
    """
    Protocol for a service that discovers dependencies of a model instance.
    """

    def discover_dependencies(self, model_instance: t.Any) -> t.Set[Dependency]:
        """
        Discover dependencies of a model instance.
        :param model_instance: The instance to analyze.
        :return: A set of dependencies related to the model instance.
        """
        raise NotImplementedError("discover_dependencies method must be implemented by subclasses.")


class CloneStrategy(t.Protocol):

    def is_suitable(self, model_instance: t.Any) -> bool:
        """
        Check if the strategy is suitable for cloning the given model instance.
        :param model_instance: The instance to check.
        :return: True if the strategy can handle this instance, False otherwise.
        """
        raise NotImplementedError("is_suitable method must be implemented by subclasses.")

    def clone(self, model_instance: t.Any) -> t.Any:
        """
        Clone a model instance.
        :param model_instance: The instance to clone.
        :return: A new instance of the same type with the same data.
        """
        raise NotImplementedError("Clone method must be implemented by subclasses.")


class IdResolver(t.Protocol):
    """
    Protocol for a service that resolves the ID of a model instance.
    This is used to ensure that cloned instances have unique identifiers.
    """

    def __call__(self, model_instance: t.Any) -> str:
        """
        Resolve the ID of a model instance.
        :param model_instance: The instance for which to resolve the ID.
        :return: A unique identifier for the instance.
        """
        raise NotImplementedError("resolve_id method must be implemented by subclasses.")


class CloneService(t.Protocol):
    """
    Protocol for a service that handles cloning of model instances.
    """
    strategies: t.Set[CloneStrategy]
    dependencies_discovery: DependencyDiscoveryService
    logger: logging.Logger
    history_log: CloneLogger
    id_resolver: IdResolver

    def __init__(self, instance: t.Any, strategies: t.Set[CloneStrategy],
                 dependencies_discovery: DependencyDiscoveryService) -> None:
        self.instance = instance
        self.strategies = strategies
        self.dependencies_discovery = dependencies_discovery
        self.logger = logging.getLogger("game.service.clone")

    def clone(self, model_instance: t.Any, deep=True) -> t.Any:
        identifier = self.id_resolver(model_instance)
        if self.history_log.is_cloned(model_instance, identifier):
            raise AlreadyClonedError(
                f"Instance {model_instance} with ID {id(model_instance)} has already been cloned."
            )
        for strategy in self.strategies:
            if strategy.is_suitable(model_instance):
                new_instance = strategy.clone(model_instance)
                self.history_log.cloned(model_instance, identifier)
                if deep:
                    self.clone_dependencies(model_instance, new_instance)
                return new_instance
        raise CannotCloneError(f"No suitable strategy found for cloning {type(model_instance).__name__}.")

    def clone_dependencies(self, original_instance: t.Any, target_instance: t.Any) -> None:
        for dependency in self.dependencies_discovery.discover_dependencies(original_instance):
            try:
                cloned_dependency = self.clone(dependency.instance)
                dependency.assigner(target_instance, cloned_dependency)
                self.logger.info(
                    f"Cloned dependency {dependency.instance} for {type(original_instance).__name__}."
                )
                self.clone_dependencies(dependency.instance, cloned_dependency)
            except AlreadyClonedError:
                self.logger.debug(
                    f"Dependency {dependency.instance} for {type(original_instance).__name__} has already been cloned."
                )
            except CannotCloneError:
                self.logger.warning(
                    f"Cannot clone dependency {dependency.instance} for {type(original_instance).__name__}."
                )
