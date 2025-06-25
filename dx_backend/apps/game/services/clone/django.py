import copy
import logging
import typing as t

from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField
from django.db.models.fields.reverse_related import ManyToOneRel, OneToOneRel

from .base import (
    Dependency, DependencyDiscoveryService, CloneStrategy, CloneLogger, IdResolver, AlreadyClonedError,
    CannotCloneError, FilterDependency, AcceptAllDependencies
)


class DjangoIdResolver:
    """Resolves Django model instance IDs."""

    def __call__(self, model_instance: models.Model) -> str:
        return f"{model_instance._meta.label}:{model_instance.pk}"


class DjangoCloneLogger:
    """Tracks cloned Django model instances."""

    def __init__(self):
        self.history: t.Dict[t.Any, t.Set[str]] = {}

    def cloned(self, model_instance: t.Any, instance_id: str) -> None:
        if model_instance not in self.history:
            self.history[model_instance] = set()
        self.history[model_instance].add(instance_id)

    def is_cloned(self, model_instance: t.Any, instance_id: str) -> bool:
        return model_instance in self.history and instance_id in self.history[model_instance]

    def reset(self):
        """Clear clone history."""
        self.history.clear()


class DjangoFieldAssigner:
    """Handles Django field assignments post-clone."""

    @staticmethod
    def set_foreign_key(parent_instance: models.Model, child_instance: models.Model, field_name: str):
        setattr(parent_instance, field_name, child_instance)
        parent_instance.save(update_fields=[field_name])

    @staticmethod
    def set_reverse_foreign_key(parent_instance: models.Model, child_instance: models.Model, field_name: str):
        setattr(child_instance, field_name, parent_instance)
        child_instance.save(update_fields=[field_name])

    @staticmethod
    def add_many_to_many(parent_instance: models.Model, child_instance: models.Model, field_name: str):
        getattr(parent_instance, field_name).add(child_instance)


class DjangoDependencyDiscoveryService:
    """Django model dependency discovery via field introspection."""

    def __init__(self, clone_related: bool = True, reverse: bool = True, dependency_filter: "FilterDependency" = None):
        self.related = clone_related
        self.clone_reverse = reverse
        self.dependency_filter = dependency_filter or AcceptAllDependencies()

    def discover_dependencies(self, model_instance: models.Model) -> t.Set[Dependency]:
        dependencies = set()

        if self.related:
            dependencies.update(self._discover_forward_relations(model_instance))

        if self.clone_reverse:
            dependencies.update(self._discover_reverse_relations(model_instance))

        return dependencies

    def _discover_forward_relations(self, instance: models.Model) -> t.Set[Dependency]:
        dependencies = set()

        for field in instance._meta.get_fields():
            if isinstance(field, (ForeignKey, OneToOneField)):
                related_instance = getattr(instance, field.name, None)
                if related_instance:
                    assigner = lambda parent, child, fn=field.name: (
                        DjangoFieldAssigner.set_foreign_key(parent, child, fn)
                    )
                    dep = Dependency(related_instance, assigner)
                    if self.dependency_filter(dep):
                        dependencies.add(Dependency(related_instance, assigner))
                        continue
                    logging.getLogger("game.service.clone").debug(
                        f"Skipping dependency {related_instance} for {instance} due to filter."
                    )
            elif isinstance(field, ManyToManyField):
                m2m_manager = getattr(instance, field.name)
                for related_instance in m2m_manager.all():
                    assigner = lambda parent, child, fn=field.name: (
                        DjangoFieldAssigner.add_many_to_many(parent, child, fn)
                    )
                    if self.dependency_filter(Dependency(related_instance, assigner)):
                        dependencies.add(Dependency(related_instance, assigner))
                        continue
                    logging.getLogger("game.service.clone").debug(
                        f"Skipping dependency {related_instance} for {instance} due to filter."
                    )
        return dependencies

    def _discover_reverse_relations(self, instance: models.Model) -> t.Set[Dependency]:
        dependencies = set()

        for field in instance._meta.get_fields():
            if isinstance(field, (ManyToOneRel, OneToOneRel)):
                try:
                    dependency_instance = getattr(instance, field.get_accessor_name(), None)
                except ObjectDoesNotExist:
                    continue
                if dependency_instance:
                    try:
                        if isinstance(field, ManyToOneRel):
                            related_manager = getattr(instance, field.get_accessor_name())
                            for related_instance in related_manager.all():
                                assigner = lambda parent, child, fn=field.field.name: (
                                    DjangoFieldAssigner.set_reverse_foreign_key(parent, child, fn)
                                )
                                dependency = Dependency(related_instance, assigner)
                                if self.dependency_filter(dependency):
                                    dependencies.add(dependency)
                                    continue
                                logging.getLogger("game.service.clone").debug(
                                    f"Skipping dependency {related_instance} for {instance} due to filter."
                                )

                        elif isinstance(field, OneToOneRel):
                            related_instance = getattr(instance, field.get_accessor_name(), None)
                            if related_instance:
                                assigner = lambda parent, child, fn=field.field.name: (
                                    DjangoFieldAssigner.set_reverse_foreign_key(parent, child, fn)
                                )
                                dependency = Dependency(related_instance, assigner)
                                if self.dependency_filter(dependency):
                                    dependencies.add(dependency)
                                    continue
                                logging.getLogger("game.service.clone").debug(
                                    f"Skipping dependency {related_instance} for {instance} due to filter."
                                )
                    except AttributeError:
                        pass  # Relation doesn't exist
                    except ObjectDoesNotExist:
                        pass
                    except Exception as e:
                        logging.getLogger("game.service.clone").error(
                            f"Error discovering reverse relation {field.get_accessor_name()} for {instance}: {e}"
                        )
                        raise

        return dependencies


class DjangoModelCloneStrategy:
    """Standard Django model cloning strategy."""

    def is_suitable(self, model_instance: t.Any) -> bool:
        return isinstance(model_instance, models.Model)

    def clone(self, model_instance: models.Model) -> models.Model:
        new_instance = copy.deepcopy(model_instance)
        new_instance.pk = None
        try:
            new_instance.save()
        except Exception as e:
            logging.getLogger("game.service.clone").error(
                f"Failed to save cloned instance of {type(model_instance).__name__}: {e}"
            )
            raise CannotCloneError(f"Could not save cloned instance: {e}")
        return new_instance


class DjangoPolymorphicCloneStrategy:
    """Polymorphic Django model cloning strategy."""

    def is_suitable(self, model_instance: t.Any) -> bool:
        try:
            from polymorphic.models import PolymorphicModel
            return isinstance(model_instance, PolymorphicModel)
        except ImportError:
            return False

    def clone(self, model_instance: models.Model) -> models.Model:
        concrete_class = model_instance.__class__
        field_values = {}

        for field in concrete_class._meta.fields:
            if field.primary_key or (field.unique and not isinstance(field, (ForeignKey, OneToOneField))):
                continue

            field_values[field.name] = getattr(model_instance, field.name)

        new_instance = concrete_class(**field_values)
        new_instance.save()

        for field in concrete_class._meta.many_to_many:
            original_m2m = getattr(model_instance, field.name)
            new_m2m = getattr(new_instance, field.name)
            new_m2m.set(original_m2m.all())

        return new_instance


class ExcludePolymorphicCloneStrategy:
    """Strategy to exclude polymorphic models from cloning."""

    def is_suitable(self, model_instance: t.Any) -> bool:
        try:
            from polymorphic.models import PolymorphicModel
            return isinstance(model_instance, PolymorphicModel)
        except ImportError:
            return False

    def clone(self, model_instance: models.Model) -> models.Model:
        raise CannotCloneError("Polymorphic models are excluded from cloning.")


class ExcludeNonTaggedCloneStrategyDjangoModelCloneStrategy:
    """Strategy to exclude models without specific tags from cloning."""

    def __init__(self, required_tag: str):
        self.required_tag = required_tag

    def is_suitable(self, model_instance: t.Any) -> bool:
        return hasattr(model_instance, 'game_tags') and self.required_tag not in model_instance.game_tags

    def clone(self, model_instance: models.Model) -> models.Model:
        raise CannotCloneError(
            f"Model {model_instance} does not have the required tag '{self.required_tag}' for cloning.")


class DjangoCloneService:
    """Django implementation of CloneService protocol."""

    def __init__(self,
                 strategies: t.Set[CloneStrategy] = None,
                 dependencies_discovery: DependencyDiscoveryService = None,
                 history_log: CloneLogger = None,
                 id_resolver: IdResolver = None):

        self.strategies = strategies or {
            ExcludePolymorphicCloneStrategy(),
            DjangoModelCloneStrategy()
        }
        self.dependencies_discovery = dependencies_discovery or DjangoDependencyDiscoveryService()
        self.history_log = history_log or DjangoCloneLogger()
        self.id_resolver = id_resolver or DjangoIdResolver()
        self.logger = logging.getLogger("game.service.clone")

    @transaction.atomic
    def clone(self, model_instance: models.Model, deep: bool = True) -> models.Model:
        identifier = self.id_resolver(model_instance)

        if self.history_log.is_cloned(model_instance, identifier):
            raise AlreadyClonedError(
                f"Instance {model_instance} with ID {identifier} has already been cloned."
            )

        for strategy in self.strategies:
            if strategy.is_suitable(model_instance):
                new_instance = strategy.clone(model_instance)
                if not new_instance:
                    continue
                self.history_log.cloned(model_instance, identifier)

                if deep:
                    self.clone_dependencies(model_instance, new_instance)

                self.logger.info(f"Cloned {type(model_instance).__name__} id={model_instance.pk}")
                return new_instance

        raise CannotCloneError(f"No suitable strategy found for cloning {type(model_instance).__name__}.")

    def clone_dependencies(self, original_instance: models.Model, target_instance: models.Model) -> None:
        dependencies = self.dependencies_discovery.discover_dependencies(original_instance)

        for dependency in dependencies:
            try:
                cloned_dependency = self.clone(dependency.instance, deep=True)
                if dependency.assigner:
                    dependency.assigner(target_instance, cloned_dependency)

                self.logger.debug(
                    f"Assigned cloned {type(dependency.instance).__name__} to {type(target_instance).__name__}"
                )
            except AlreadyClonedError:
                self.logger.debug(
                    f"Dependency {dependency.instance} for {type(original_instance).__name__} already cloned."
                )
            except CannotCloneError:
                self.logger.warning(
                    f"Cannot clone dependency {dependency.instance} for {type(original_instance).__name__}."
                )

    def reset_history(self):
        """Reset clone history for fresh cloning session."""
        if hasattr(self.history_log, 'reset'):
            self.history_log.reset()


# Factory functions
def create_django_clone_service(clone_related: bool = True, clone_reverse: bool = True) -> DjangoCloneService:
    """Create configured Django clone service."""
    discovery = DjangoDependencyDiscoveryService(clone_related=clone_related, reverse=clone_reverse)
    return DjangoCloneService(dependencies_discovery=discovery)


def clone_campaign_deep(campaign_instance: models.Model) -> models.Model:
    """Clone campaign with full dependency tree."""
    service = create_django_clone_service()
    try:
        return service.clone(campaign_instance, deep=True)
    except (AlreadyClonedError, CannotCloneError) as e:
        logging.getLogger("game.service.clone").error(f"Clone failed: {e}")
        raise
    finally:
        service.reset_history()
