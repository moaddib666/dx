"""
Model Graph Discovery Engine - Pure Domain Logic
Stack-based traversal with cycle prevention.
"""

import dataclasses
import logging
import typing as t
from abc import abstractmethod
from collections import deque
from enum import StrEnum

# ============================================================================
# Domain Models
# ============================================================================
logger = logging.getLogger("apps.game.services.clone.discovery")


class RelationType(StrEnum):
    FOREIGN_KEY = "foreign_key"
    ONE_TO_ONE = "one_to_one"
    MANY_TO_MANY = "many_to_many"
    REVERSE_FOREIGN_KEY = "reverse_foreign_key"
    REVERSE_ONE_TO_ONE = "reverse_one_to_one"
    REVERSE_MANY_TO_MANY = "reverse_many_to_many"


@dataclasses.dataclass(frozen=True)
class RelationshipMetadata:
    field_name: t.Optional[str] = None
    related_name: t.Optional[str] = None
    through_model: t.Optional[t.Type] = None
    null: bool = True
    blank: bool = True
    on_delete: t.Optional[str] = None


@dataclasses.dataclass(frozen=True)
class ModelDependency:
    model_class: t.Type
    app_label: str
    model_name: str

    def __repr__(self):
        return f"ModelDependency({self.app_label}.{self.model_name})"


@dataclasses.dataclass(frozen=True)
class ModelRelation:
    source: ModelDependency
    target: ModelDependency
    relation_type: RelationType
    metadata: RelationshipMetadata

    @property
    def is_reverse_relation(self) -> bool:
        return self.relation_type in {
            RelationType.REVERSE_FOREIGN_KEY,
            RelationType.REVERSE_ONE_TO_ONE,
            RelationType.REVERSE_MANY_TO_MANY
        }


@dataclasses.dataclass
class ModelGraph:
    nodes: t.Set[ModelDependency] = dataclasses.field(default_factory=set)
    edges: t.Set[ModelRelation] = dataclasses.field(default_factory=set)
    root_models: t.Set[ModelDependency] = dataclasses.field(default_factory=set)

    def add_model(self, model_dependency: ModelDependency) -> None:
        self.nodes.add(model_dependency)

    def add_relation(self, source: ModelDependency, target: ModelDependency,
                     relation_type: RelationType, metadata: RelationshipMetadata) -> None:
        relation = ModelRelation(source, target, relation_type, metadata)
        self.edges.add(relation)
        self.add_model(source)
        self.add_model(target)

    def get_relations_for_model(self, model_dependency: ModelDependency) -> t.List[ModelRelation]:
        return [edge for edge in self.edges if edge.source == model_dependency]


# ============================================================================
# Stack Infrastructure
# ============================================================================

@dataclasses.dataclass
class StackNode:
    model_class: t.Type
    depth: int
    next_node: t.Optional['StackNode'] = None


class ExplicitStack:
    def __init__(self):
        self._head: t.Optional[StackNode] = None
        self._size = 0

    def push(self, model_class: t.Type, depth: int = 0) -> None:
        new_node = StackNode(model_class, depth, self._head)
        self._head = new_node
        self._size += 1

    def pop(self) -> t.Optional[StackNode]:
        if not self._head:
            return None
        node = self._head
        self._head = self._head.next_node
        self._size -= 1
        return node

    def is_empty(self) -> bool:
        return self._head is None


@dataclasses.dataclass(frozen=True)
class EdgeKey:
    source_model: str
    field_name: str
    target_model: str

    @classmethod
    def from_relation(cls, relation: ModelRelation) -> 'EdgeKey':
        return cls(
            source_model=f"{relation.source.app_label}.{relation.source.model_name}",
            field_name=relation.metadata.field_name or "",
            target_model=f"{relation.target.app_label}.{relation.target.model_name}"
        )


# ============================================================================
# Protocols
# ============================================================================

class FilterModel(t.Protocol):
    @abstractmethod
    def __call__(self, model_dependency: ModelDependency, relation: t.Optional[ModelRelation] = None) -> bool:
        ...


class RelationExtractor(t.Protocol):
    @abstractmethod
    def extract_relations(self, model_class: t.Type) -> t.List[ModelRelation]:
        ...


# ============================================================================
# Core Discovery Engine
# ============================================================================

class GraphTraversalEngine:
    def __init__(self):
        self.node_map: t.Dict[t.Type, ModelDependency] = {}
        self.visited_edges: t.Set[EdgeKey] = set()
        self.discovered_relations: t.List[ModelRelation] = []
        self.stack = ExplicitStack()
        self.breadth_queue = deque()

    def build_graph(self, root_models: t.List[t.Type], relation_extractor: RelationExtractor,
                    filter_func: t.Optional[FilterModel] = None, max_depth: int = 10) -> ModelGraph:

        # Initialize with root models
        for model in root_models:
            self._add_to_node_map(model)
            self.breadth_queue.append((model, 0))

        # BFS + stack traversal
        while self.breadth_queue:
            model_class, depth = self.breadth_queue.popleft()
            if depth >= max_depth:
                continue
            self._discover_model_relations(model_class, depth, relation_extractor, filter_func)

        return self._build_final_graph(root_models)

    def _add_to_node_map(self, model_class: t.Type) -> ModelDependency:
        if model_class not in self.node_map:
            self.node_map[model_class] = ModelDependency(
                model_class=model_class,
                app_label=model_class._meta.app_label,
                model_name=model_class._meta.model_name
            )
        return self.node_map[model_class]

    def _discover_model_relations(self, model_class: t.Type, current_depth: int,
                                  relation_extractor: RelationExtractor, filter_func: t.Optional[FilterModel]) -> None:
        self.stack.push(model_class, current_depth)

        while not self.stack.is_empty():
            node = self.stack.pop()
            source_dependency = self._add_to_node_map(node.model_class)
            relations = relation_extractor.extract_relations(node.model_class)

            for relation in relations:
                edge_key = EdgeKey.from_relation(relation)
                if edge_key in self.visited_edges:
                    continue

                self.visited_edges.add(edge_key)

                if filter_func and not filter_func(relation.target, relation):
                    continue

                target_dependency = self._add_to_node_map(relation.target.model_class)
                self.discovered_relations.append(relation)

                next_depth = current_depth + 1
                self.breadth_queue.append((relation.target.model_class, next_depth))

    def _build_final_graph(self, root_models: t.List[t.Type]) -> ModelGraph:
        graph = ModelGraph()

        for dependency in self.node_map.values():
            graph.add_model(dependency)

        for model in root_models:
            if model in self.node_map:
                graph.root_models.add(self.node_map[model])

        for relation in self.discovered_relations:
            graph.edges.add(relation)

        return graph


# ============================================================================
# Service Interface
# ============================================================================

class ModelGraphService:
    def __init__(self, relation_extractor: RelationExtractor):
        self.relation_extractor = relation_extractor

    def discover_dependencies(self, root_models: t.List[t.Type], filter_func: t.Optional[FilterModel] = None,
                              max_depth: int = 10) -> ModelGraph:
        engine = GraphTraversalEngine()
        return engine.build_graph(root_models, self.relation_extractor, filter_func, max_depth)


# ============================================================================
# Django Relation Extractor
# ============================================================================

class DjangoRelationExtractor:
    """Django-specific relation extraction."""

    def extract_relations(self, model_class: t.Type) -> t.List[ModelRelation]:
        relations = []

        # Forward relations
        for field in model_class._meta.get_fields():
            if self._is_forward_relation(field):
                relation = self._create_forward_relation(model_class, field)
                if relation:
                    relations.append(relation)

        # Reverse relations (optional)
        for field in model_class._meta.get_fields():
            if self._is_reverse_relation(field):
                relation = self._create_reverse_relation(model_class, field)
                if relation:
                    relations.append(relation)

        return relations

    def _is_forward_relation(self, field) -> bool:
        return (hasattr(field, 'related_model') and
                field.related_model and
                not getattr(field, 'many_to_one', False))

    def _is_reverse_relation(self, field) -> bool:
        return (hasattr(field, 'related_model') and
                field.related_model and
                (getattr(field, 'one_to_many', False) or
                 getattr(field, 'one_to_one', False) or
                 getattr(field, 'many_to_many', False)))

    def _create_forward_relation(self, model_class: t.Type, field) -> t.Optional[ModelRelation]:
        if not hasattr(field, 'related_model') or not field.related_model:
            return None

        source = self._create_dependency(model_class)
        target = self._create_dependency(field.related_model)

        metadata = RelationshipMetadata(
            field_name=field.name,
            related_name=getattr(field, 'related_name', None),
            null=getattr(field, 'null', True)
        )

        relation_type = self._get_forward_type(field)
        return ModelRelation(source, target, relation_type, metadata)

    def _create_reverse_relation(self, model_class: t.Type, field) -> t.Optional[ModelRelation]:
        if not hasattr(field, 'related_model') or not field.related_model:
            return None

        source = self._create_dependency(model_class)
        target = self._create_dependency(field.related_model)

        metadata = RelationshipMetadata(
            field_name=getattr(field, 'get_accessor_name', lambda: field.name)(),
            related_name=field.name
        )

        relation_type = self._get_reverse_type(field)
        return ModelRelation(source, target, relation_type, metadata)

    def _create_dependency(self, model_class: t.Type) -> ModelDependency:
        return ModelDependency(
            model_class=model_class,
            app_label=model_class._meta.app_label,
            model_name=model_class._meta.model_name
        )

    def _get_forward_type(self, field) -> RelationType:
        field_name = field.__class__.__name__
        mapping = {
            'ForeignKey': RelationType.FOREIGN_KEY,
            'OneToOneField': RelationType.ONE_TO_ONE,
            'ManyToManyField': RelationType.MANY_TO_MANY,
        }
        return mapping.get(field_name, RelationType.FOREIGN_KEY)

    def _get_reverse_type(self, field) -> RelationType:
        if getattr(field, 'one_to_many', False):
            return RelationType.REVERSE_FOREIGN_KEY
        elif getattr(field, 'one_to_one', False):
            return RelationType.REVERSE_ONE_TO_ONE
        elif getattr(field, 'many_to_many', False):
            return RelationType.REVERSE_MANY_TO_MANY
        return RelationType.REVERSE_FOREIGN_KEY


# ============================================================================
# Filters
# ============================================================================

class AcceptAllModels(FilterModel):
    def __call__(self, model_dependency: ModelDependency, relation: t.Optional[ModelRelation] = None) -> bool:
        return True


class ExcludeModelTypes(FilterModel):
    def __init__(self, excluded_models: t.Set[t.Type]):
        self.excluded_models = excluded_models

    def __call__(self, model_dependency: ModelDependency, relation: t.Optional[ModelRelation] = None) -> bool:
        return model_dependency.model_class not in self.excluded_models


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


class CompositeFilter(FilterModel):
    """Composite filter that combines multiple filters with AND logic."""

    def __init__(self, *filters: FilterModel):
        self.filters = filters

    def __call__(self, model_dependency: ModelDependency, relation: t.Optional[ModelRelation] = None) -> bool:
        result = all(f(model_dependency, relation) for f in self.filters)
        logger.debug(
            "CompositeFilter called for %s: filters=%s, result=%s",
            model_dependency, self.filters, result
        )
        return result
