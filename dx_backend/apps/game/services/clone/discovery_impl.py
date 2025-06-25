"""
Django Model Dependency Discovery Implementation
==============================================

Django-specific implementation of model dependency discovery.
Analyzes Django model classes to discover relationships between model types.
"""

import logging
import typing as t

from django.db import models
from django.db.models import ForeignKey, OneToOneField, ManyToManyField, ManyToOneRel, OneToOneRel, ManyToManyRel

from .discovery_core import (
    RelationshipMetadata, FilterModel, ModelGraph, AcceptAllModels,
    ModelDependency, RelationType, ModelRelation
)

logger = logging.getLogger("apps.game.services.clone")


class DjangoRelationshipMetadata(RelationshipMetadata):
    """Django-specific relationship metadata."""

    @classmethod
    def from_django_field(cls, field) -> 'DjangoRelationshipMetadata':
        """Create metadata from a Django model field."""
        logger.debug("Creating relationship metadata from Django field: %r", field)
        field_name = getattr(field, 'name', None)
        related_name = getattr(field, 'related_query_name', None)
        through_model = getattr(field, 'through', None)
        null = getattr(field, 'null', True)
        blank = getattr(field, 'blank', True)
        on_delete = str(getattr(field, 'on_delete', None))
        db_column = getattr(field, 'db_column', None)

        metadata = cls(
            field_name=field_name,
            related_name=related_name,
            through_model=through_model,
            null=null,
            blank=blank,
            on_delete=on_delete,
            db_column=db_column
        )
        logger.debug("Created metadata: field_name=%r, related_name=%r, through_model=%r",
                     field_name, related_name, through_model)
        return metadata


class DjangoModelDiscoveryService:
    """
    Django-specific implementation of model dependency discovery.

    Analyzes Django model classes to discover all relationships between
    model types without touching the database or instances.
    """

    def __init__(self, include_reverse_relations: bool = True):
        """
        Initialize the Django model discovery service.

        :param include_reverse_relations: Whether to discover reverse relationships
        """
        logger.debug("Initializing DjangoModelDiscoveryService with include_reverse_relations=%s",
                     include_reverse_relations)
        self.include_reverse_relations = include_reverse_relations

    def discover_model_dependencies(self,
                                    root_models: t.List[t.Type],
                                    filter_func: t.Optional[FilterModel] = None,
                                    include_reverse_relations: t.Optional[bool] = None) -> ModelGraph:
        """
        Discover dependencies between Django model classes.

        Analyzes model fields and relationships to build a complete
        dependency graph of the schema structure.
        """
        if filter_func is None:
            logger.debug("No filter provided, using AcceptAllModels")
            filter_func = AcceptAllModels()
        else:
            logger.debug("Using provided filter: %r", filter_func)

        if include_reverse_relations is None:
            include_reverse_relations = self.include_reverse_relations

        logger.debug("Starting model dependency discovery for %d root models", len(root_models))

        graph = ModelGraph()
        visited_models = set()

        # Add root models
        for model_class in root_models:
            root_dependency = self._create_model_dependency(model_class)
            graph.root_models.add(root_dependency)
            logger.debug("Added root model: %s", root_dependency)

        # Discover dependencies recursively
        for model_class in root_models:
            self._discover_model_recursive(
                model_class=model_class,
                graph=graph,
                visited_models=visited_models,
                filter_func=filter_func,
                include_reverse_relations=include_reverse_relations
            )

        logger.debug("Completed model dependency discovery. Graph has %d models and %d relations",
                     len(graph.nodes), len(graph.edges))

        return graph

    def _create_model_dependency(self, model_class: t.Type) -> ModelDependency:
        """Create a ModelDependency from a Django model class."""
        meta = model_class._meta
        return ModelDependency(
            model_class=model_class,
            app_label=meta.app_label,
            model_name=meta.model_name
        )

    def _discover_model_recursive(self,
                                  model_class: t.Type,
                                  graph: ModelGraph,
                                  visited_models: t.Set[t.Type],
                                  filter_func: FilterModel,
                                  include_reverse_relations: bool) -> None:
        """Recursively discover model dependencies."""

        if model_class in visited_models:
            logger.debug("Model %s already visited, skipping", model_class.__name__)
            return

        logger.debug("Discovering dependencies for model: %s", model_class.__name__)
        visited_models.add(model_class)

        source_dependency = self._create_model_dependency(model_class)
        graph.add_model(source_dependency)

        # Discover forward relationships
        forward_fields = 0
        for field in model_class._meta.get_fields():
            if isinstance(field, (ForeignKey, OneToOneField)):
                logger.debug("Processing single relation field: %s", getattr(field, 'name', field))
                self._handle_single_relation_model(
                    field=field,
                    source_dependency=source_dependency,
                    graph=graph,
                    visited_models=visited_models,
                    filter_func=filter_func,
                    include_reverse_relations=include_reverse_relations
                )
                forward_fields += 1
            elif isinstance(field, ManyToManyField):
                logger.debug("Processing many-to-many field: %s", getattr(field, 'name', field))
                self._handle_many_to_many_relation_model(
                    field=field,
                    source_dependency=source_dependency,
                    graph=graph,
                    visited_models=visited_models,
                    filter_func=filter_func,
                    include_reverse_relations=include_reverse_relations
                )
                forward_fields += 1

        logger.debug("Processed %d forward relationship fields for %s", forward_fields, model_class.__name__)

        # Discover reverse relationships if enabled
        if include_reverse_relations:
            logger.debug("Processing reverse relationships for %s", model_class.__name__)
            reverse_fields = 0
            for field in model_class._meta.get_fields():
                if isinstance(field, (ManyToOneRel, OneToOneRel, ManyToManyRel)):
                    logger.debug("Processing reverse relation field: %s", getattr(field, 'name', field))
                    self._handle_reverse_relation_model(
                        field=field,
                        source_dependency=source_dependency,
                        graph=graph,
                        visited_models=visited_models,
                        filter_func=filter_func,
                        include_reverse_relations=include_reverse_relations
                    )
                    reverse_fields += 1
            logger.debug("Processed %d reverse relationship fields for %s", reverse_fields, model_class.__name__)
        else:
            logger.debug("Skipping reverse relationships (disabled) for %s", model_class.__name__)

        logger.debug("Completed recursive discovery for model: %s", model_class.__name__)

    def _handle_single_relation_model(self,
                                      field,
                                      source_dependency: ModelDependency,
                                      graph: ModelGraph,
                                      visited_models: t.Set[t.Type],
                                      filter_func: FilterModel,
                                      include_reverse_relations: bool) -> None:
        """Handle ForeignKey and OneToOne field relationships."""
        field_name = getattr(field, 'name', str(field))
        logger.debug("Handling single relation for field %s on model %s", field_name, source_dependency.model_name)

        related_model = field.related_model
        target_dependency = self._create_model_dependency(related_model)
        logger.debug("Created target dependency: %s", target_dependency)

        relation_type = (RelationType.ONE_TO_ONE if isinstance(field, OneToOneField)
                         else RelationType.FOREIGN_KEY)
        logger.debug("Relation type determined as: %s", relation_type)

        metadata = DjangoRelationshipMetadata.from_django_field(field)
        logger.debug("Created relationship metadata for field %s", field_name)

        relation = ModelRelation(
            source=source_dependency,
            target=target_dependency,
            relation_type=relation_type,
            metadata=metadata
        )
        logger.debug("Created model relation: %r", relation)

        if not filter_func(target_dependency, relation):
            logger.debug("Target model filtered out by filter_func, skipping")
            return

        logger.debug("Adding relation to graph: %s -> %s (%s)",
                     source_dependency, target_dependency, relation_type)
        graph.add_relation(source_dependency, target_dependency, relation_type, metadata)

        logger.debug("Recursively discovering dependencies for model: %s", related_model.__name__)
        self._discover_model_recursive(
            model_class=related_model,
            graph=graph,
            visited_models=visited_models,
            filter_func=filter_func,
            include_reverse_relations=include_reverse_relations
        )

    def _handle_many_to_many_relation_model(self,
                                            field,
                                            source_dependency: ModelDependency,
                                            graph: ModelGraph,
                                            visited_models: t.Set[t.Type],
                                            filter_func: FilterModel,
                                            include_reverse_relations: bool) -> None:
        """Handle ManyToMany field relationships."""
        field_name = getattr(field, 'name', str(field))
        logger.debug("Handling many-to-many relation for field %s on model %s",
                     field_name, source_dependency.model_name)

        related_model = field.related_model
        target_dependency = self._create_model_dependency(related_model)
        logger.debug("Created target dependency: %s", target_dependency)

        relation_type = (
            RelationType.MANY_TO_MANY_THROUGH if hasattr(field, 'through') and not field.through._meta.auto_created
            else RelationType.MANY_TO_MANY)
        logger.debug("Relation type determined as: %s", relation_type)

        metadata = DjangoRelationshipMetadata.from_django_field(field)
        logger.debug("Created relationship metadata for field %s", field_name)

        relation = ModelRelation(
            source=source_dependency,
            target=target_dependency,
            relation_type=relation_type,
            metadata=metadata
        )
        logger.debug("Created model relation: %r", relation)

        if not filter_func(target_dependency, relation):
            logger.debug("Target model filtered out by filter_func, skipping")
            return

        logger.debug("Adding relation to graph: %s -> %s (%s)",
                     source_dependency, target_dependency, relation_type)
        graph.add_relation(source_dependency, target_dependency, relation_type, metadata)

        logger.debug("Recursively discovering dependencies for model: %s", related_model.__name__)
        self._discover_model_recursive(
            model_class=related_model,
            graph=graph,
            visited_models=visited_models,
            filter_func=filter_func,
            include_reverse_relations=include_reverse_relations
        )

    def _handle_reverse_relation_model(self,
                                       field,
                                       source_dependency: ModelDependency,
                                       graph: ModelGraph,
                                       visited_models: t.Set[t.Type],
                                       filter_func: FilterModel,
                                       include_reverse_relations: bool) -> None:
        """Handle reverse relationships."""
        logger.debug("Handling reverse relation for field %r on model %s", field, source_dependency.model_name)

        related_model = field.related_model
        target_dependency = self._create_model_dependency(related_model)
        logger.debug("Created target dependency: %s", target_dependency)

        if isinstance(field, ManyToOneRel):
            relation_type = RelationType.REVERSE_FOREIGN_KEY
        elif isinstance(field, OneToOneRel):
            relation_type = RelationType.REVERSE_ONE_TO_ONE
        elif isinstance(field, ManyToManyRel):
            relation_type = RelationType.REVERSE_MANY_TO_MANY
        else:
            logger.debug("Unknown reverse relation type: %s, skipping", type(field))
            return

        logger.debug("Relation type determined as: %s", relation_type)

        accessor_name = field.get_accessor_name()
        metadata = DjangoRelationshipMetadata(
            field_name=accessor_name,
            related_name=field.name
        )
        logger.debug("Created relationship metadata with field_name=%s, related_name=%s",
                     accessor_name, field.name)

        relation = ModelRelation(
            source=source_dependency,
            target=target_dependency,
            relation_type=relation_type,
            metadata=metadata
        )
        logger.debug("Created model relation: %r", relation)

        if not filter_func(target_dependency, relation):
            logger.debug("Target model filtered out by filter_func, skipping")
            return

        logger.debug("Adding relation to graph: %s -> %s (%s)",
                     source_dependency, target_dependency, relation_type)
        graph.add_relation(source_dependency, target_dependency, relation_type, metadata)

        logger.debug("Recursively discovering dependencies for model: %s", related_model.__name__)
        self._discover_model_recursive(
            model_class=related_model,
            graph=graph,
            visited_models=visited_models,
            filter_func=filter_func,
            include_reverse_relations=include_reverse_relations
        )
