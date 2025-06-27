import dataclasses
import logging
import typing

from django.db.models import Model

from apps.game.services.clone.base import Dependency, DependencyFactory
from apps.game.services.clone.clone_strategy import CloneStrategy
from apps.game.services.clone.related_objects_fetch import FieldRelationFetcher, get_default_relations_fetcher

logger = logging.getLogger("apps.game.services.clone")


@dataclasses.dataclass(frozen=True)
class History:
    set_of_instances: set[Model] = dataclasses.field(default_factory=set)

    def is_visited(self, instance: Model) -> bool:
        return instance in self.set_of_instances

    def add(self, instance: Model):
        self.set_of_instances.add(instance)

    def get_all(self) -> set[Model]:
        return self.set_of_instances


class InstanceDependencyGraph:
    history: History
    deps_factory: DependencyFactory
    dependencies: list[Dependency]
    field_relation_fetcher: FieldRelationFetcher

    def __init__(self, instance: Model, relation_fetcher: FieldRelationFetcher = None):
        self.instance = instance
        self.history = History()
        self.deps_factory = DependencyFactory()
        self.dependencies: list[Dependency] = []
        self.relation_fetcher: FieldRelationFetcher = relation_fetcher or get_default_relations_fetcher()

    def discover(self):
        """
        Discover all dependencies starting from the given instance.
        This method will traverse the model's relations and build a dependency graph.
        """
        self.history.add(self.instance)
        self.discover_dependent_instances(self.instance, 0)
        return self.dependencies

    def discover_dependent_instances(self, instance: Model, layer: int):
        """
        find instances that have one to one or foreign key relations to the instance
        or many-to-many relations with the current instance
        """
        logger.debug(f"Discovering dependencies for {instance.__class__.__name__} {instance.pk} at layer {layer}")
        all_related_instances = set()
        for field in instance._meta.get_fields():
            # only auto created fields are included
            if not field.auto_created:
                continue
            if not field.is_relation:
                continue
            logger.debug(f"Processing [{layer}] field: {field.name} on {instance.__class__.__name__}")
            instances = self.fetch_instances_by_field(instance, field)
            for related_instance in instances:
                if self.history.is_visited(related_instance):
                    logger.debug(
                        f"Horizon [{layer}] already visited: {related_instance.__class__.__name__} {related_instance.pk}")
                    dependency = self.deps_factory.create_reverse_dependency(
                        source=instance,
                        target=related_instance,
                        layer=layer + 1,
                        field=field,
                    )
                    self.dependencies.append(dependency)
                    continue
                all_related_instances.add(related_instance)
                self.history.add(related_instance)
                dependency = self.deps_factory.create_reverse_dependency(
                    source=instance,
                    target=related_instance,
                    layer=layer,
                    field=field,
                )
                self.dependencies.append(dependency)

        for related_instance in all_related_instances:
            self.discover_dependent_instances(related_instance, layer + 1)

    def fetch_instances_by_field(self, instance: Model, field: typing.Any) -> typing.Iterable[Model]:
        """
        Process auto-created fields and return related instances.
        The field can be a ManyToOne, ManyToMany, or OneToOne relation.
        """
        # Dirty hack better to crete proper abstraction for this
        if field.name == "gameobject_ptr":
            # Skip the gameobject_ptr field as it is not a relation
            return []
        return self.relation_fetcher.fetch(instance, field)


class InstanceDeepCloner:
    dependencies: typing.Iterable[Dependency]
    strategy: CloneStrategy

    def __init__(self, root_instance: Model, dependencies: typing.Iterable[Dependency], strategy: CloneStrategy):
        self.dependencies = dependencies
        self.strategy = strategy
        self.root_instance = self.strategy.clone_root_instance(root_instance)
        self.root_instance.save()

    def clone_root_instance(self, instance: Model) -> Model:
        instance = self.strategy.clone_root_instance(instance)
        return instance

    def sort_dependencies(self):
        """
        Sort dependencies based on their layer to ensure that dependencies are processed in the correct order.
        This is important for cloning to ensure that dependencies are resolved correctly.
        """
        self.dependencies = sorted(self.dependencies, key=lambda dep: dep.layer)

    def clone(self):
        """
        Clone all instances based on the discovered dependencies.
        This method will use the provided cloning strategy to clone each instance.
        """
        self.sort_dependencies()
        for dependency in self.dependencies:
            self.strategy.apply(dependency)
