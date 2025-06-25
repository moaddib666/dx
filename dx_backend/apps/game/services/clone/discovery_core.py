"""
Model Dependency Discovery System - Core Abstractions
===================================================

This module provides abstract protocols for discovering dependencies
between model classes. It focuses solely on discovering and mapping
relationships between model types at the schema level.
"""

import dataclasses
import logging
import typing as t
from abc import abstractmethod
from enum import StrEnum

logger = logging.getLogger("apps.game.services.clone")


class RelationType(StrEnum):
    """Abstract relationship types between models."""
    FOREIGN_KEY = "foreign_key"
    ONE_TO_ONE = "one_to_one"
    MANY_TO_MANY = "many_to_many"
    REVERSE_FOREIGN_KEY = "reverse_foreign_key"
    REVERSE_ONE_TO_ONE = "reverse_one_to_one"
    REVERSE_MANY_TO_MANY = "reverse_many_to_many"
    MANY_TO_MANY_THROUGH = "many_to_many_through"


@dataclasses.dataclass(frozen=True)
class RelationshipMetadata:
    """Metadata about a relationship between model classes."""
    field_name: t.Optional[str] = None
    related_name: t.Optional[str] = None
    through_model: t.Optional[t.Type] = None
    null: bool = True
    blank: bool = True
    on_delete: t.Optional[str] = None
    db_column: t.Optional[str] = None


@dataclasses.dataclass(frozen=True)
class ModelDependency:
    """Represents a model class dependency."""
    model_class: t.Type
    app_label: str
    model_name: str

    def __post_init__(self):
        logger.debug("Created ModelDependency for %s.%s", self.app_label, self.model_name)

    def __repr__(self):
        return f"ModelDependency({self.app_label}.{self.model_name})"


@dataclasses.dataclass(frozen=True)
class ModelRelation:
    """Represents a relationship between two model classes."""
    source: ModelDependency
    target: ModelDependency
    relation_type: RelationType
    metadata: RelationshipMetadata

    def __post_init__(self):
        logger.debug("Created ModelRelation: %s -> %s (%s)",
                     self.source, self.target, self.relation_type)

    @property
    def is_reverse_relation(self) -> bool:
        """Check if this is a reverse relationship."""
        return self.relation_type in {
            RelationType.REVERSE_FOREIGN_KEY,
            RelationType.REVERSE_ONE_TO_ONE,
            RelationType.REVERSE_MANY_TO_MANY
        }

    @property
    def is_many_relation(self) -> bool:
        """Check if this represents a one-to-many or many-to-many relationship."""
        return self.relation_type in {
            RelationType.REVERSE_FOREIGN_KEY,
            RelationType.MANY_TO_MANY,
            RelationType.REVERSE_MANY_TO_MANY,
            RelationType.MANY_TO_MANY_THROUGH
        }

    def __repr__(self):
        field_info = f" via {self.metadata.field_name}" if self.metadata.field_name else ""
        return f"ModelRelation({self.source} -> {self.target} [{self.relation_type}]{field_info})"


@dataclasses.dataclass
class ModelGraph:
    """Graph representing model class dependencies and their relationships."""
    nodes: t.Set[ModelDependency] = dataclasses.field(default_factory=set)
    edges: t.Set[ModelRelation] = dataclasses.field(default_factory=set)
    root_models: t.Set[ModelDependency] = dataclasses.field(default_factory=set)

    def add_model(self, model_dependency: ModelDependency) -> None:
        """Add a model dependency node to the graph."""
        logger.debug("Adding model to graph: %s", model_dependency)
        self.nodes.add(model_dependency)
        logger.debug("Graph now has %d model nodes", len(self.nodes))

    def add_relation(self,
                     source: ModelDependency,
                     target: ModelDependency,
                     relation_type: RelationType,
                     metadata: RelationshipMetadata) -> None:
        """Add a relationship edge to the graph."""
        logger.debug("Adding model relation: %s -> %s (%s)", source, target, relation_type)

        relation = ModelRelation(
            source=source,
            target=target,
            relation_type=relation_type,
            metadata=metadata
        )

        self.edges.add(relation)
        self.add_model(source)
        self.add_model(target)
        logger.debug("Graph now has %d model relations", len(self.edges))

    def get_relations_for_model(self, model_dependency: ModelDependency) -> t.List[ModelRelation]:
        """Get all relations where the model is the source."""
        logger.debug("Getting relations for model: %s", model_dependency)
        relations = [edge for edge in self.edges if edge.source == model_dependency]
        logger.debug("Found %d relations for model %s", len(relations), model_dependency)
        return relations

    def get_relations_by_type(self, relation_type: RelationType) -> t.List[ModelRelation]:
        """Get all relations of a specific type."""
        logger.debug("Getting relations of type: %s", relation_type)
        relations = [edge for edge in self.edges if edge.relation_type == relation_type]
        logger.debug("Found %d relations of type %s", len(relations), relation_type)
        return relations

    def get_models_by_app(self, app_label: str) -> t.List[ModelDependency]:
        """Get all models from a specific app."""
        logger.debug("Getting models from app: %s", app_label)
        models = [model for model in self.nodes if model.app_label == app_label]
        logger.debug("Found %d models in app %s", len(models), app_label)
        return models


class FilterModel(t.Protocol):
    """Protocol for filtering discovered model dependencies."""

    @abstractmethod
    def __call__(self, model_dependency: ModelDependency, relation: t.Optional[ModelRelation] = None) -> bool:
        """
        Filter model dependencies based on a condition.

        :param model_dependency: The model dependency to check
        :param relation: The relation that discovered this dependency (if any)
        :return: True if the model should be included, False otherwise
        """
        ...


class ModelDiscoveryService(t.Protocol):
    """Protocol for discovering dependencies between model classes."""

    @abstractmethod
    def discover_model_dependencies(self,
                                    root_models: t.List[t.Type],
                                    filter_func: t.Optional[FilterModel] = None,
                                    include_reverse_relations: bool = True) -> ModelGraph:
        """
        Discover dependencies between model classes.

        :param root_models: The root model classes to start discovery from
        :param filter_func: Optional filter to apply during discovery
        :param include_reverse_relations: Whether to include reverse relationships
        :return: A model dependency graph
        """
        ...


class AcceptAllModels(FilterModel):
    """Filter that accepts all model dependencies without any condition."""

    def __call__(self, model_dependency: ModelDependency, relation: t.Optional[ModelRelation] = None) -> bool:
        logger.debug("AcceptAllModels filter called for %s", model_dependency)
        return True


class ExcludeModelTypes(FilterModel):
    """Filter that excludes specific model classes."""

    def __init__(self, excluded_models: t.Set[t.Type]):
        logger.debug("Creating ExcludeModelTypes filter with %d excluded models", len(excluded_models))
        self.excluded_models = excluded_models

    def __call__(self, model_dependency: ModelDependency, relation: t.Optional[ModelRelation] = None) -> bool:
        result = model_dependency.model_class not in self.excluded_models
        logger.debug("ExcludeModelTypes filter for %s: %s", model_dependency, result)
        return result


class ExcludeRelationTypes(FilterModel):
    """Filter that excludes models discovered through specific relation types."""

    def __init__(self, excluded_relation_types: t.Set[RelationType]):
        logger.debug("Creating ExcludeRelationTypes filter with excluded types: %s", excluded_relation_types)
        self.excluded_relation_types = excluded_relation_types

    def __call__(self, model_dependency: ModelDependency, relation: t.Optional[ModelRelation] = None) -> bool:
        if relation is None:
            logger.debug("ExcludeRelationTypes filter for %s: True (no relation)", model_dependency)
            return True
        result = relation.relation_type not in self.excluded_relation_types
        logger.debug("ExcludeRelationTypes filter for %s with relation type %s: %s",
                     model_dependency, relation.relation_type, result)
        return result


class CompositeFilter(FilterModel):
    """Combine multiple model filters with AND logic."""

    def __init__(self, filters: t.List[FilterModel]):
        logger.debug("Creating CompositeFilter with %d filters", len(filters))
        self.filters = filters

    def __call__(self, model_dependency: ModelDependency, relation: t.Optional[ModelRelation] = None) -> bool:
        logger.debug("CompositeFilter called for %s", model_dependency)
        result = all(f(model_dependency, relation) for f in self.filters)
        logger.debug("CompositeFilter result for %s: %s", model_dependency, result)
        return result


class TagsFilter(FilterModel):
    """Filter that checks if a model has a specific tag.
       Example:
           TagsFilter(
            required_tags=[TagsDescriptor.BaseTags.CAMPAIGN_TEMPLATE],
            exclude_tags=[],
        )
    """

    def __init__(self, required_tags: t.List[str] = None, exclude_tags: t.Optional[t.List[str]] = None):
        self.required_tags = set(required_tags or set())
        self.exclude_tags = set(exclude_tags or set())

    def __call__(self, model_dependency: ModelDependency, relation: t.Optional[ModelRelation] = None) -> bool:
        model_tags = getattr(model_dependency.model_class, 'game_tags', [])
        result = (
                self.required_tags.issubset(model_tags) and
                not self.exclude_tags.intersection(model_tags)
        )
        logger.debug(
            "TagsFilter called for %s: required_tags=%s, exclude_tags=%s, result=%s",
            model_dependency, self.required_tags, self.exclude_tags, result
        )
        return result
